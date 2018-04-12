import webapp2
import os
from google.appengine.ext.webapp import template
import json
from assets.scripts.dbproxy import dbProxy 
from assets.scripts.dbdata import *

class MainPage(webapp2.RequestHandler):
	def get(self):
		#elf.response.headers['Content-Type'] = 'text/plain'
		#self.response.write('Hello, World!')
		self.path = 'index.html'
		f = open(self.path) 
		self.response.out.write(f.read())

class SearchHandler(webapp2.RequestHandler):
	def post(self):
		results = self.searchForItem(self.request.body)
		#self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(results))

	def searchForItem(self, data):
		jsonData = json.loads(data)
		brand = jsonData["brand"]
		zipCode = jsonData["zip"]
		model = jsonData["model"]
		# THIS WILL CHANGE (LOCATION OF DB)
		# use this for deployed mysql:
		proxy = dbProxy('/cloudsql/itemeyes-199123:us-central1:itemeyes', 0, True)
		# use this for local mysql:
		#proxy = dbProxy('127.0.0.1', 3307)
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

class AddHandler(webapp2.RequestHandler):
	def post(self):
		results = self.addItem(self.request.body)
		#self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(results))

	def addItem(self, data):
		jsonData = json.loads(data)
		brand = jsonData["brand"]
		model = jsonData["model"]
		company = jsonData["company"]
		address = jsonData["address"]
		city = jsonData["city"]
		state = jsonData["state"]
		zipCode = jsonData["zip"]
		token = jsonData["token"]
		# use this for deployed mysql:
		proxy = dbProxy('/cloudsql/itemeyes-199123:us-central1:itemeyes', 0, True)
		# use this for local mysql:
		#proxy = dbProxy('127.0.0.1', 3307)
		userID = proxy.queryUsersByToken(token)

		if (userID=="no!"):
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

class LoginHandler(webapp2.RequestHandler):
	def post(self):
		results = self.login(self.request.body)
		#self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(results))

	def login(self, data):
		# check username/passHash combo
		# if not, return some error
		# if yes, return username in JSON form
		jsonData = json.loads(data)
		username = jsonData["username"]
		passHash = jsonData["passHash"]
		# use this for deployed mysql:
		proxy = dbProxy('/cloudsql/itemeyes-199123:us-central1:itemeyes', 0, True)
		# use this for local mysql:
		#proxy = dbProxy('127.0.0.1', 3307)
		results = proxy.queryUsers(username, passHash)
		if (results == "no!"):
			results = ""
		jsonAccessToken = {}
		jsonAccessToken['token'] = results
		return jsonAccessToken

class CreateHandler(webapp2.RequestHandler):
	def post(self):
		results = self.create(self.request.body)
		#self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(results))

	def create(self, data):
		#check if username already in db
		# if not, add it with names, passhash, username
		jsonData = json.loads(data)
		firstName = jsonData["firstName"]
		lastName = jsonData["lastName"]
		username = jsonData["username"]
		passHash = jsonData["passHash"]
		# use this for deployed mysql:
		proxy = dbProxy('/cloudsql/itemeyes-199123:us-central1:itemeyes', 0, True)
		# use this for local mysql:
		#proxy = dbProxy('127.0.0.1', 3307)
		newUser = User(firstName, lastName, username, passHash)
		addUser = proxy.addUser(newUser)
		if (addUser == "no!"):
			addUser = "" 
		jsonAccessToken = {}
		jsonAccessToken['token'] = addUser
		return jsonAccessToken

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/search', SearchHandler),
	('/add',AddHandler),
	('/login',LoginHandler),
	('/create',CreateHandler),

], debug=True)