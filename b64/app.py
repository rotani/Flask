# -*- coding: utf-8 -*-
'''
#5539 new task
FlaskでBase64エンコード/デコードアプリ
''' 
import os
from flask import Flask, render_template, request, session, \
  redirect, url_for

from sqlalchemy import create_engine, Column, Integer, String, \
    Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from werkzeug.utils import secure_filename

import sqlite3
import hashlib
import base64

app = Flask(__name__)
app.secret_key = b'random string...'

dbpath = '' #'sqlite:////xxx/usr.db'
engine = create_engine(dbpath)

# base model
Base = declarative_base()

# model class
class User(Base):
  __tablename__ = 'users'
    
  id = Column(Integer, primary_key=True)
  name = Column(String(255))
  password = Column(String(255))

  def to_dict(self):
    return {
        'id':int(self.id), 
        'name':str(self.name), 
        'password':str(self.password)
    }


@app.route('/', methods=['GET'])
def index():
  return render_template('messages.html',
                         login=False,
                         title='Base64エンコード/デコード',
                         message='Not Logined...',
                         data=[])
                         
# login form sended.
@app.route('/login', methods=['POST'])
def login_post():
  # 送信されたnameとpasswordを取り出す
  name = request.form.get('name')
  pswd = request.form.get('password')
  # salt + ハッシュ化
  md5 = hashlib.md5()
  md5.update(name.encode("utf-8"))
  salt = md5.digest()[-1* len(name):]
  md5.update(pswd.encode('utf-8') + salt)
  pswd = md5.hexdigest()

  # Sessionオブジェクトの準備
  Session = sessionmaker(bind=engine)
  ses = Session()
  # Userのパスワードと送信されたパスワードが等しいか確認する
  usr = ses.query(User).filter(User.name == name).one()
  if pswd == usr.password:
    flg = str(usr.id)
  else:
    flg = 'False'  
    ses.close()
  return flg
 
@app.route('/encode', methods=['POST'])
def encode():
  msg = request.form.get('message')
  enc =base64.b64encode(msg.encode())
  return enc.decode("utf-8")
 
@app.route('/decode', methods=['POST'])
def decode():
  msg = request.form.get('message')
  dec =base64.b64decode(msg.encode())
  return dec.decode("utf-8")

if __name__ == "__main__":
    app.run()
