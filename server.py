#  coding: utf-8
import socketserver
import os
from pathlib import Path
# Copyright 2022 Kaixuan Hu
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        request = self.data.decode("utf-8");
        lines = request.splitlines()
        command = lines[0].split(" ")[0]
        http = lines[0].split(" ")[2]
        url = lines[0].split(" ")[1]
        css_file = False #default http file

        #handle command other than GET
        if(command != "GET"):
            response = http + " 405 Method Not Allowed\r\n"
            response += "\r\n"
            self.request.send(response.encode("utf-8"))
        else:
            #only allow serving files under /www or deeper
            p1 = os.path.realpath(os.getcwd() + "/www" + url)
            p2 = os.path.realpath(os.getcwd() + "/www")
            if(p1 != p2 and not p1.startswith(p2 + os.sep)):
                response = http + " 404 Not Found\r\n"
                response += "\r\n"
                #print(response)
                self.request.send(response.encode("utf-8"))
                return
            if(url[-5:] == ".html" or url[-1] == "/" or url[-4:] == ".css"):
                if(url[-1] == "/"):
                    url += "index.html"

                if(url[-4:] == ".css"):
                    css_file = True

                try:
                    f = open(os.getcwd() + "/www" + url,"rb")
                except:
                    response = http + " 404 Not Found\r\n"
                    response += "\r\n"
                    self.request.send(response.encode("utf-8"))
                else:
                    html_content = f.read()
                    f.close()
                    response = http + " 200 OK\r\n"
                    if(css_file):
                        response += "Content-Type: text/css\r\n"
                    else:
                        response += "Content-Type: text/html\r\n"
                    response += "\r\n"
                    self.request.send(response.encode("utf-8"))
                    self.request.send(html_content)
            else:
                response = http + " 301 Moved Permanently\r\n"
                response += "Location: "
                response += url
                response += "/\r\n" #add "/"
                self.request.send(response.encode("utf-8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
