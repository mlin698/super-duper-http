# HTTP Server

#### What you need to get started:
- python3

#### Running the script:
- In one terminal, enter the following command to start the server. If no port is specified, the server will default to port 80.
  - `python3 HTTPServer.py [port]`
  - Upon execution, this script will ask for a location for the passwd and group files. If no file is specified, the locations will default to /etc/passwd and /etc/group
  
- In another terminal, enter the following command to start the client. This is where we enter our GET commands. The server location should look something like: `http://localhost:80`.
  - `python3 Client.py [server location]`
  
- In the Client, you can then query the server.

#### Supported commands:
