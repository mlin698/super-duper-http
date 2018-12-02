# HTTP Server

### What you need to get started:
python3

### Running the script:
In one terminal, enter the following command to start the server. If no port is specified, the server will default to port 80.

`python3 HTTPServer.py [port]`

Upon execution, this script will ask for a location for the passwd and group files. If no file is specified, the locations will default to /etc/passwd and /etc/group
  
In another terminal, enter the following command to start the client. This is where we enter our GET commands. The server location should look something like: `http://localhost:80`.

`python3 Client.py [server location]`
  
In the Client, you can then query the server. If any queries return empty, you will get a 404 not found response. If any queries are invalid, the command window running the Server will throw an exception.

### Supported commands:

#### GET /users
Returns all users, as defined in the passwd file.

#### GET /users/\<uid\>
Returns user with matching uid. Example: `GET /users/90`

#### Get /users/\<uid\>/groups
Returns any group that the user with that particular uid is a member of. Example: `GET /users/90/groups`

#### GET /users/query[?name=\<name\>][&uid=\<uid\>][&gid=\<gid\>][&comment=\<comment\>][&home=\<home_path\>][&shell=\<shell_path\>]
Returns any user matching the query parameters. Example: `GET /users/query?name=megan&uid=90&shell=%2Fusr%2Fbin%2Ffalse`

Please note that when entering a path, replace all `/` with `%2F`

#### GET /groups
Returns all groups, as defined in the group file.

#### GET /groups/\<gid\>
Returns group with matching gid. Example: `GET /groups/40`

#### GET /groups/query[?name=\<name\>][&gid=\<gid\>][&member=\<member1\>[&member=\<member2\>][&. ..]]
Returns any group matching the query parameters. Example: `GET /groups/query?name=work&member=megan&member=ryan`


