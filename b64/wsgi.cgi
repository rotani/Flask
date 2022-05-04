#!/home/denebola/.pyenv/versions/3.9.1/bin/python
# -*- coding: utf-8 -*-
import wsgiref.handlers
from http.server import BaseHTTPRequestHandler

if __name__ == '__main__':
  from app import app
  wsgiref.handlers.CGIHandler().run(app)
