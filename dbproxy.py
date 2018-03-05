#!/usr/bin/python
import MySQLdb

class dbProxy():
	def __init__(self, host):
		self.db = MySQLdb.connect(host=host,
					user="root",
					passwd="root")
		self.cur = self.db.cursor()

	def addUser(self, newUser):
		self.cur.execute("Use ItemEyes")
		addUserQuery = ("INSERT INTO Users "
					"(firstName, lastName, username) "
					"VALUES (%s, %s, %s)")
		dataUser = (newUser.firstName, newUser.lastName, newUser.username)
		self.cur.execute(addUserQuery, dataUser)
		self.db.commit()
		print("added user")
		newUser.userID = self.cur.lastrowid
		#return self.cur.lastrowid

	def addItem(self, newItem):
		self.cur.execute("Use ItemEyes")
		addItem = ("INSERT INTO Items "
					"(brand, model) "
					"VALUES (%s, %s)")
		dataItem = (newItem.brand, newItem.model)
		self.cur.execute(addItem, dataItem)
		itemID = self.cur.lastrowid
		self.db.commit()
		newItem.itemID = self.cur.lastrowid
		print("added item")

		addMapQuery = ("INSERT INTO ItemMap "
					"(clmapID, itemID, userID) "
					"VALUES (%s, %s, %s)")
		dataMap = (newItem.mapID, itemID, newItem.userID)
		self.cur.execute(addMapQuery, dataMap)
		print("added map")
		self.db.commit()
		

	def addCompany(self, newCompany):
		self.cur.execute("Use ItemEyes")
		addCompanyQuery = ("INSERT INTO Companies "
						"(companyName) "
						"VALUES (%s)")
		self.cur.execute(addCompanyQuery, (newCompany.companyName,))
		self.db.commit()
		print("added company")
		newCompany.companyID = self.cur.lastrowid
		#return self.cur.lastrowid

	def addLocation(self, newLocation):
		self.cur.execute("Use ItemEyes")
		addLocationQuery = ("INSERT INTO Locations "
						"(streetAddress, city, state, zip) "
						"VALUES (%s, %s, %s, %s)")
		dataLocation = (newLocation.streetAddress, newLocation.city, newLocation.state, newLocation.zipCode)
		self.cur.execute(addLocationQuery,dataLocation)
		print("added location")
		newLocation.locationID = self.cur.lastrowid
		self.db.commit()

		addMapQuery = ("INSERT INTO CompanyLocationMap "
					"(companyID, locationID) "
					"VALUES (%s, %s)")
		dataMap = (newLocation.companyID, newLocation.locationID)
		self.cur.execute(addMapQuery, dataMap)
		print("added map")
		self.db.commit()
		return self.cur.lastrowid
		
	def queryItems(self, item, city):
		# return results as json object
		return queryResults