#!/usr/bin/python
# acts as proxy between JavaScript and database

import MySQLdb
import random, string
import os

class dbProxy():
	def __init__(self, host, port, useAppEngine):
		print(port)	
		if (useAppEngine):
			self.db = MySQLdb.connect(
				unix_socket=host,
				user="root",
				passwd="root")
		else:
			if (host=="127.0.0.1"):
				port=3306	
			if (port != 0):
				self.db = MySQLdb.connect(
					host=host,
					user="root",
					passwd="root",
					port=port)
			else:
				self.db = MySQLdb.connect(host=host,
							user="root",
							passwd="root")
		self.cur = self.db.cursor()

	def randomWord(self, length):
		letters = string.ascii_lowercase
		return ''.join(random.choice(letters) for i in range(length))

	def queryUsersByToken(self, token):
		self.cur.execute("Use ItemEyes")
		userQuery = ("SELECT Users.userID FROM Users WHERE Users.accessToken = %s")
		tokenData = (token,)
		self.cur.execute(userQuery, tokenData)
		results = self.cur.fetchone()
		if (results):
			return results
		else:
			return "no!"

	def queryUsers(self, username, passHash):
		self.cur.execute("Use ItemEyes")
		userQuery = ("SELECT * FROM Users WHERE Users.username = %s AND Users.passHash = %s")
		queryData = (username, passHash)
		self.cur.execute(userQuery, queryData)
		results = self.cur.fetchone()
		if (results):
			token = self.randomWord(128)
			self.addToken(token, username)
			return token
		else:
			return "no!"

	def addToken(self, token, username):
		self.cur.execute("Use ItemEyes")
		tokenInsert = ("UPDATE Users SET Users.accessToken = %s WHERE Users.username = %s")
		tokenValues = (token, username)
		self.cur.execute(tokenInsert, tokenValues)
		self.db.commit()
		return

	def addUser(self, newUser):
		self.cur.execute("Use ItemEyes")
		checkUsers = ("SELECT * FROM Users WHERE Users.username = %s")
		userData = (newUser.username,)
		self.cur.execute(checkUsers, userData)
		results = self.cur.fetchone()
		if (results):
			return "no!"

		token = self.randomWord(128)
		addUserQuery = ("INSERT INTO Users "
					"(firstName, lastName, username, passHash, accessToken) "
					"VALUES (%s, %s, %s, %s, %s)")
		dataUser = (newUser.firstName, newUser.lastName, newUser.username, newUser.passHash, token)
		self.cur.execute(addUserQuery, dataUser)
		self.db.commit()
		return token
		#newUser.userID = self.cur.lastrowid
		#return self.cur.lastrowid

	def addItem(self, newItem):
		self.cur.execute("Use ItemEyes")
		# first check if item is already in there!
		itemCheck = ("SELECT Items.itemID FROM Items WHERE Items.brand = %s AND Items.model = %s")
		itemData = (newItem.brand, newItem.model)
		self.cur.execute(itemCheck, itemData)
		results = self.cur.fetchone()
		if (results):
			newItem.itemID = results
		else:		
			addItem = ("INSERT INTO Items "
						"(brand, model) "
						"VALUES (%s, %s)")
			dataItem = (newItem.brand, newItem.model)
			self.cur.execute(addItem, dataItem)
			newItem.itemID = self.cur.lastrowid
			self.db.commit()

		# now check if item is already mapped to the given location/company
		mapCheck = ("SELECT ItemMap.itemMapID FROM ItemMap WHERE itemID = %s AND clmapID = %s")
		mapData = (newItem.itemID, newItem.clmapID)
		self.cur.execute(mapCheck, mapData)
		results = self.cur.fetchone()
		if (results):
			return

		# not currently mapped!
		addMapQuery = ("INSERT INTO ItemMap "
					"(clmapID, itemID, userID) "
					"VALUES (%s, %s, %s)")
		dataMap = (newItem.clmapID, newItem.itemID, newItem.userID)
		self.cur.execute(addMapQuery, dataMap)
		self.db.commit()
		

	def addCompany(self, newCompany):
		self.cur.execute("Use ItemEyes")
		#first check if company already there
		checkCompanies = ("SELECT Companies.companyID FROM Companies WHERE companyName = %s")
		companyData = (newCompany.companyName,)
		self.cur.execute(checkCompanies, companyData)
		results = self.cur.fetchone()
		if (results):
			return results

		#if it wasn't there, insert it!
		addCompanyQuery = ("INSERT INTO Companies "
						"(companyName) "
						"VALUES (%s)")
		self.cur.execute(addCompanyQuery, (newCompany.companyName,))
		self.db.commit()
		newCompany.companyID = self.cur.lastrowid
		return newCompany.companyID

	def addLocation(self, newLocation):
		# first check if location already exists
		locationCheck = ("SELECT Locations.locationID FROM Locations WHERE Locations.streetAddress = %s AND Locations.city = %s AND Locations.state = %s AND Locations.zip = %s")
		locationData = (newLocation.streetAddress, newLocation.city, newLocation.state, newLocation.zipCode)
		self.cur.execute(locationCheck, locationData)
		results = self.cur.fetchone()
		if (results):
			newLocation.locationID = results
		else:
			# if location not in there, put it in!
			self.cur.execute("Use ItemEyes")
			addLocationQuery = ("INSERT INTO Locations "
							"(streetAddress, city, state, zip) "
							"VALUES (%s, %s, %s, %s)")
			dataLocation = (newLocation.streetAddress, newLocation.city, newLocation.state, newLocation.zipCode)
			self.cur.execute(addLocationQuery,dataLocation)
			newLocation.locationID = self.cur.lastrowid
			self.db.commit()

		#check companylocation map!
		checkMap = ("SELECT CompanyLocationMap.clmapID FROM CompanyLocationMap WHERE companyID = %s AND locationID = %s")
		mapData = (newLocation.companyID, newLocation.locationID)
		self.cur.execute(checkMap, mapData)
		results = self.cur.fetchone()
		if (results):
			return results

		# if not in there, add it!
		addMapQuery = ("INSERT INTO CompanyLocationMap "
					"(companyID, locationID) "
					"VALUES (%s, %s)")
		dataMap = (newLocation.companyID, newLocation.locationID)
		self.cur.execute(addMapQuery, dataMap)
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
		
