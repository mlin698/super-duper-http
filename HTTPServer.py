#!/usr/bin/env python
# coding: utf-8
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from sys import argv
from collections import OrderedDict

passwd_info = list()
group_info = list()
class Server(BaseHTTPRequestHandler):
    def set_headers(self, response=200):
        self.send_response(response)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    #parse the password file for the information we want
    def parse_passwd(self):
        '''
        example: _reportmemoryexception:*:269:269:ReportMemoryException:/var/db/reportmemoryexception:/usr/bin/false
        name:passwd:userid:groupid:comment:home:shell
        {“name”: “root”, “uid”: 0, “gid”: 0, “comment”: “root”, “home”: “/root”, “shell”: “/bin/bash”}
        '''
        f = open(passwd_path, 'r')
        for line in f:
            #ignore header
            if line.startswith('#'):
                continue
            info = line.split(':')
            #if file is malformed
            if len(info) != 7:
                raise Exception('passwd file is not formatted correctly')
            info.pop(1) #drop password field
            info[5] = info[5].rstrip('\n')
            passwd_info.append(info)

        f.close()
        return

    #parse the group file
    def parse_group(self):
        '''
        nobody:*:-2:
        groupname:passwd:groupid:grouplist
        '''
        f = open(group_path, 'r')
        for line in f:
            #ignore header
            if line.startswith('#'):
                continue
            info = line.split(':')
            #if file is malformed
            if len(info) != 4:
                raise Exception('group file is not formatted correctly')
            info.pop(1) #drop password field
            info[2] = info[2].rstrip('\n')
            group_info.append(info)

        f.close()
        return

    def parse_query(self, query):
        return

    #{“name”: “root”, “uid”: 0, “gid”: 0, “comment”: “root”, “home”: “/root”, “shell”: “/bin/bash”}
    def format_passwd(self, values):
        format = ['name', 'uid', 'gid', 'comment', 'home', 'shell']
        ret_passwd = list()
        for row in values:
            temp = {}
            for i in range(len(row)):
                temp[format[i]] = row[i]
            ret_passwd.append(temp)

        return ret_passwd
        
    #{“name”: “_analyticsusers”, “gid”: 250, “members”: [“_analyticsd’,”_networkd”,”_timed”]}
    def format_group(self, values):
        format = ['name', 'gid', 'members']
        ret_group = list()
        for row in values:
            temp = {}
            for i in range(len(row)):
                temp[format[i]] = row[i]
            ret_group.append(temp)

        return ret_group

    def do_GET(self):
        self.set_headers()
        self.parse_passwd()
        self.parse_group()

        #GET request path, passed in from client
        command = self.path

        if command == '/users':
            ret = self.format_passwd(passwd_info)
        elif command == '/groups':
            ret = self.format_passwd(group_info)
        else:
            raise Exception('Invalid query')

        ret = str(ret).encode()
        self.wfile.write(ret)


def run(server_class=HTTPServer, handler_class=Server, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    #default value at /etc/passwd
    print('Input path to passwd file:')
    passwd_input = input()

    if passwd_input != '':
        #TODO: while input is not valid(aka path doesn't exist), ask to try again
        passwd_path = passwd_input
    else:
        #passwd_path = '/etc/passwd'
        passwd_path = 'passwd_test'

    #default value at /etc/group
    print('Input path to group file:')
    group_input = input()

    if group_input != '':
        group_path = group_input
    else:
        #group_path = '/etc/group'
        group_path = 'group_test'


    if len(argv) == 2:
        print(argv[1])
        run(port=int(argv[1]))
    else:
        run()
