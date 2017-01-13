#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import pymysql
import argparse

class querySphinx:
  def __init__(self, port='9303', host='127.0.0.1', query="show tables"):
    self.sphinxhost = host
    self.sphinxport = port
    self.query = query

  def run_check(self):
    try:
      connection = pymysql.connect(host=self.sphinxhost, port=self.sphinxport)
      cursor = connection.cursor()
      cursor.execute(self.query)
      connection.close()
      return True
    except:
      return False

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
# GET
  def do_GET(self):
    params = self.path.split('/')
    sphinxhost = params[1]
    sphinxport = int(params[2])

    # perform sphinx check
    checker = querySphinx(port=sphinxport, host=sphinxhost)
    # Send response status code
    if checker.run_check():
      self.send_response(200)
    else:
      self.send_response(503)

    # Send headers
    self.send_header('Content-type','text/html')
    self.end_headers()

    return

  def do_HEAD(self):
    # Send response status code
    self.send_response(200)

    # Send headers
    self.send_header('Content-type','text/html')
    self.end_headers()

  def log_message(self, format, *args):
    return

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-a", "--address", type=str, default='127.0.0.1',
                      help="ip address to listen, default=127.0.0.1")
  parser.add_argument("-p", "--port", type=int, default='8081',
                      help='port to listen, default=8081')
  args = parser.parse_args()
  print('starting server...')
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = (args.address, args.port)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

if __name__ == "__main__":
    main()
