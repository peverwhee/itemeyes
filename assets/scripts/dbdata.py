
class User():
	def __init__(self, first, last, username, passHash):
		self.firstName = first
		self.lastName = last
		self.username = username
		self.passHash = passHash
		self.accessToken = ""
		self.userID = -1

class Item():
	def __init__(self, brand, model, userID, mapID):
		self.brand = brand
		self.model = model
		self.userID = userID
		self.clmapID = mapID
		self.itemID = -1

class Company():
	def __init__(self, name):
		self.companyName = name
		self.companyID = -1

class Location():
	def __init__(self, street, city, state, zipCode, companyID):
		self.streetAddress = street
		self.city = city
		self.state = state
		self.zipCode = zipCode
		self.companyID = companyID
		self.locationID = -1
