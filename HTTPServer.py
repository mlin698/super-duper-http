#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        #TODO: throw error if file is not correctly formatted
        f = open(path)

        self.wfile.write(f.read())
        f.close()

def run(server_class=HTTPServer, handler_class=Server, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    #default value at /etc/passwd
    print('Input path to passwd file:')
    input = raw_input()

    if input != '':
        #TODO: while input is not valid, ask to try again
        path = input
    else:
        path = '/etc/passwd'

    #TODO: must check if path actually exists

    run()
