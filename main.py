import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class SearchHandler(webapp2.RequestHandler):
	def post(self):
		results = searchForItem(self.request.body)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.dumps(results))

	def searchForItem(data):
	    jsonData = json.loads(data)
	    brand = jsonData["brand"]
	    zipCode = jsonData["zip"]
	    model = jsonData["model"]
	    # THIS WILL CHANGE (LOCATION OF DB)
	    proxy = dbProxy('104.197.164.53')
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
		results = addItem(self.request.body)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.dumps(results))

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
	    proxy = dbProxy('104.197.164.53')
	    userID = proxy.queryUsersByToken(token)

	    # add company if not already in there; get companyID for mapping
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
		results = login(self.request.body)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.dumps(results))

	def login(data):
	    # check username/passHash combo
	    # if not, return some error
	    # if yes, return username in JSON form
	    jsonData = json.loads(data)
	    username = jsonData["username"]
	    passHash = jsonData["passHash"]
	    proxy = dbProxy('104.197.164.53')
	    results = proxy.queryUsers(username, passHash)
	    if (results == "no!"):
	        results = ""
	    jsonAccessToken = {}
	    jsonAccessToken['token'] = results
	    return jsonAccessToken

class CreateHandler(webapp2.RequestHandler):
	def post(self):
		results = create(self.request.body)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(json.dumps(results))

	def create(data):
	    #check if username already in db
	    # if not, add it with names, passhash, username
	    jsonData = json.loads(data)
	    firstName = jsonData["firstName"]
	    lastName = jsonData["lastName"]
	    username = jsonData["username"]
	    passHash = jsonData["passHash"]
	    proxy = dbProxy('104.197.164.53')
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