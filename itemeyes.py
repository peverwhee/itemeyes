#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import os
from os import curdir, sep 

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #self._set_headers()
        if self.path == '/':
            self.path = '/index.html'
        print(self.path)
        if self.path.endswith(".html"):
            mimetype='text/html'
            sendReply = True
        if self.path.endswith(".jpg"):
            mimetype='image/jpg'
            sendReply = True
        if self.path.endswith(".gif"):
            mimetype='image/gif'
            sendReply = True
        if self.path.endswith(".js"):
            mimetype='application/javascript'
            sendReply = True
        if self.path.endswith(".css"):
            mimetype='text/css'
            sendReply = True

        if sendReply == True:
            #Open the static file requested and send it
            f = open(curdir + sep + self.path) 
            self.send_response(200)
            self.send_header('Content-type',mimetype)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(post_data)
        jsonResponse = handlePostRequest(self.path, post_data)
        self._set_headers()
        #convert json Response to string and pass into here
        self.wfile.write(json.dumps(jsonResponse))

def handlePostRequest(path, data):
    if(path == "/search"):
        return searchForItem(data)

def searchForItem(data):
    jsonData = json.loads(data)
    print(jsonData["item"])
    print(jsonData["city"])
    jsonSearchResult = {}
    jsonSearchResult['company'] = "Cuties R Us"
    jsonSearchResult['location'] = "Guam"
    #call dbproxy.queryItems(item, city)
    jsonArray = [jsonSearchResult]
    jsonSearchResults = {}
    jsonSearchResults['rows'] = jsonArray
    return jsonSearchResults
   


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

def main():
    print(os.getcwd())
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

if __name__ == "__main__":
    main()

