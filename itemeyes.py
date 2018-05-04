#!/usr/bin/env python
# main file for Compute and Kubernetes

import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import os
from os import curdir, sep
from assets.scripts.dbproxy import dbProxy 
from assets.scripts.dbdata import *
import datetime

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #self._set_headers()
        if self.path == '/':
            self.path = '/index.html'

        if self.path.endswith(".html"):
            mimetype='text/html'
            sendReply = True
        elif self.path.endswith(".jpg"):
            mimetype='image/jpg'
            sendReply = True
        elif self.path.endswith(".gif"):
            mimetype='image/gif'
            sendReply = True
        elif self.path.endswith(".js"):
            mimetype='application/javascript'
            sendReply = True
        elif self.path.endswith(".css"):
            mimetype='text/css'
            sendReply = True
        else:
            sendReply = False
            print("Not sending response for " + self.path)

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
        jsonResponse = handlePostRequest(self.path, post_data)
        self._set_headers()
        #convert json Response to string and pass into here
        self.wfile.write(json.dumps(jsonResponse))

def handlePostRequest(path, data):

    if(path == "/search"):
        return searchForItem(data)
    elif(path == "/add"):
        return addItem(data)
    elif(path == "/login"):
        return login(data)
    elif(path == "/create"):
        return create(data)

def create(data):
    #check if username already in db
    # if not, add it with names, passhash, username
    jsonData = json.loads(data)
    firstName = jsonData["firstName"]
    lastName = jsonData["lastName"]
    username = jsonData["username"]
    passHash = jsonData["passHash"]
    proxy = dbProxy(dbHost, 0, False)
    newUser = User(firstName, lastName, username, passHash)
    addUser = proxy.addUser(newUser)
    if (addUser == "no!"):
        addUser = ""
    jsonAccessToken = {}
    jsonAccessToken['token'] = addUser
    return jsonAccessToken

def login(data):
    # check username/passHash combo
    # if not, return some error
    # if yes, return username in JSON form
    jsonData = json.loads(data)
    username = jsonData["username"]
    passHash = jsonData["passHash"]
    proxy = dbProxy(dbHost, 0, False)
    results = proxy.queryUsers(username, passHash)
    if (results == "no!"):
        results = ""
    jsonAccessToken = {}
    jsonAccessToken['token'] = results
    return jsonAccessToken


def searchForItem(data):
    jsonData = json.loads(data)
    brand = jsonData["brand"]
    zipCode = jsonData["zip"]
    model = jsonData["model"]
    proxy = dbProxy(dbHost, 0, False)
    results = proxy.queryItems(brand, model, zipCode)
    jsonSearchResults = {}
    rows = []
    for result in results:
        jsonSearchResult = {}
        jsonSearchResult['company'] = result[0]
        jsonSearchResult['location'] = result[1]
        rows.append(jsonSearchResult)
    
    jsonSearchResults['rows'] = rows
    return jsonSearchResults
   
def addItem(data):
    jsonData = json.loads(data)
    brand = jsonData["brand"]
    model = jsonData["model"]
    company = jsonData["company"]
    address = jsonData["address"]
    city = jsonData["city"]
    state = jsonData["state"]
    zipCode = jsonData["zip"]
    token = jsonData["token"]
    proxy = dbProxy(dbHost, 0, False)
    userID = proxy.queryUsersByToken(token)
    if (userID=="no!"):
        jsonSearchResults={}
        jsonSearchResults['item'] = ""

    # add company if not already in there; get companyID for mapping
    else:
        newCompany = Company(company)
        companyID = proxy.addCompany(newCompany)

        # add location if not already in there; get locationID for mapping
        newLocation = Location(address,city,state,zipCode,companyID)
        clmapID = proxy.addLocation(newLocation)

        # add item if not already there!
        newItem = Item(brand,model,userID, clmapID)
        proxy.addItem(newItem)

        jsonSearchResults = {}
        jsonSearchResults['item'] = brand
    return jsonSearchResults

    #finish this for adding company, then location, then item


def run(dbHost, server_class=HTTPServer, handler_class=S, port=80):
    #handler_class.setDbHost(dbHost)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

dbHost = ""

def main():
    from sys import argv
    global dbHost
    dbHost = argv[1]

    run(dbHost)

if __name__ == "__main__":
    main()

