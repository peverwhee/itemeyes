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
		queryCheck = ("SELECT itemID FROM Items WHERE brand = %s AND model = %s")
		self.cur.execute(queryCheck, (newItem.brand, newItem.model))
		results = self.cur.fetchone()
		if (results):
			newItem.itemID = results[0]
			print("item already exists")
		else:
			addItem = ("INSERT INTO Items "
						"(brand, model) "
						"VALUES (%s, %s)")
			dataItem = (newItem.brand, newItem.model)
			self.cur.execute(addItem, dataItem)
			self.db.commit()
			newItem.itemID = self.cur.lastrowid
			print("added item")

		addMapQuery = ("INSERT INTO ItemMap "
					"(clmapID, itemID, userID) "
					"VALUES (%s, %s, %s)")
		dataMap = (newItem.mapID, newItem.itemID, newItem.userID)
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
		
	def queryItems(self, brand, model, zipCode):
		# return results as two strings
		resultsArray = []
		self.cur.execute("USE ItemEyes")
		if model:
			itemQuery = ("SELECT itemID FROM Items WHERE brand = %s AND model LIKE %s")
			model = '%' + model + '%'
			itemData = (brand, model)
		else:
			itemQuery = ("SELECT itemID FROM Items WHERE brand = %s")
			itemData = (brand,)
		self.cur.execute(itemQuery, itemData)
		results = self.cur.fetchall()
		itemIDs = []
		if (results):
			for result in results:
				itemIDs.append(result)
		else:
			temp = []
			temp.append("none")
			temp.append("none")
			resultsArray.append(temp)
			return resultsArray
		locationQuery = ("SELECT locationID FROM Locations WHERE zip = %s")
		self.cur.execute(locationQuery, (zipCode,))
		results = self.cur.fetchall()
		
		tempResultsArray = []
		if (results):
			for result in results:
				for item in itemIDs:
					query = ("SELECT locationID FROM CompanyLocationMap INNER JOIN (ItemMap) ON (ItemMap.itemID = %s AND ItemMap.clmapID = CompanyLocationMap.clmapID AND CompanyLocationMap.locationID = %s)")
					self.cur.execute(query, (item, result[0]))
					res = self.cur.fetchone()
					if (res):
						tempResultsArray.append(res[0])
		
		for result in tempResultsArray:
			query = ("SELECT streetAddress FROM Locations WHERE locationID = %s")
			self.cur.execute(query, (result,))
			address = self.cur.fetchone()[0]
			temp = []
			query = ("SELECT companyName FROM Companies INNER JOIN (CompanyLocationMap) ON (CompanyLocationMap.locationID = %s AND CompanyLocationMap.companyID = Companies.companyID)")
			self.cur.execute(query, (result,))
			company = self.cur.fetchone()[0]
			temp.append(company)
			temp.append(address)
			resultsArray.append(temp)
		if (len(tempResultsArray) == 0):
			temp = []
			temp.append("none")
			temp.append("none")
			resultsArray.append(temp)

		return resultsArray