#!/usr/bin/env python
# coding: utf-8
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from sys import argv

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
        passwd_info = list()
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
        return passwd_info

    #parse the group file
    def parse_group(self):
        '''
        nobody:*:-2:
        groupname:passwd:groupid:grouplist
        '''
        group_info = list()
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
        return group_info

    #get all the fields that we are querying
    def parse_query(self, type, query):
        user_fields = {'name', 'uid', 'gid', 'comment', 'home', 'shell'}
        group_fields = {'name', 'gid', 'members'}

        parameters = query.split('&') #['name=megan', 'gid=90']
        query_match = dict()
        for parameter in parameters:
            key = parameter.split('=')[0]
            #make sure key is valid
            if type == 'users' and key not in user_fields:
                raise Exception('Invalid query field: ' + key)
            elif type == 'groups' and key not in group_fields:
                raise Exception('Invalid group field: ' + key)

            value = parameter.split('=')[1]
            query_match[key] = value

        return query_match

    def match_query(self, type, queries):
        ret = list()
        #pick file to parse depending on the query
        if type == 'users':
            file = self.formatted_passwd
        elif type == 'groups':
            file = self.formatted_group

        for entry in file:
            flag = True #keep track of if a user fits all the queries
            for query in queries:
                #if any one of the fields don't match, we won't include that entry in the result
                if entry[query] != queries[query]:
                    flag = False
            if flag == True:
                ret.append(entry)

        return ret

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
                #format members to display like the output
                if i == 2:
                    temp[format[i]] = list()
                    members = row[i].split(',')
                    for m in members:
                        temp[format[i]].append(str(m))
                    continue
                temp[format[i]] = row[i]
            ret_group.append(temp)

        return ret_group

    #GET function
    def do_GET(self):
        self.set_headers()
        #parse all files and format them properly
        self.passwd_info = self.parse_passwd()
        self.group_info = self.parse_group()
        self.formatted_passwd = self.format_passwd(self.passwd_info)
        self.formatted_group = self.format_group(self.group_info)

        #GET request path, passed in from client
        command = self.path

        #in case you wanted to view the information dumped in a browser
        if command == '/':
            ret = self.formatted_passwd + self.formatted_group

        elif command == '/users':
            ret = self.formatted_passwd

        elif command == '/groups':
            ret = self.formatted_group

        elif command.startswith('/users/query'): #example command would be GET /users/query?name=megan&gid=90
            query = command.split('?')[1]
            queries = self.parse_query('users', query)
            ret = self.match_query('users', queries)

        elif command.startswith('/groups/query'):
            query = command.split('?')[1]
            queries = self.parse_query('groups', query)
            ret = self.match_query('groups', queries)

        else:
            raise Exception('Invalid query: ' + command)

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
