#!/usr/bin/python
import MySQLdb

class CreateDB():
	def __init__(self):
		db = MySQLdb.connect(host="localhost",
					user="root",
					passwd="root")

		self.cur = db.cursor()
		self.cur.execute("DROP DATABASE ItemEyes")
		print("dropped database")
		self.cur.execute("CREATE DATABASE IF NOT EXISTS ItemEyes")
		print("added new")
		self.cur.execute("USE ItemEyes")
		self.setupTables()
		
		self.cur.close()
		db.commit()
		db.close()

	def setupTables(self):

		TABLES = [
			"CREATE TABLE `Users` ("
			"`userID` int(11) NOT NULL AUTO_INCREMENT,"
			"`firstName` char(40),"
			"`lastName` char(40),"
			"`username` char(40) NOT NULL,"
			"`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
			"`passHash` char(32) NOT NULL,"
			"`accessToken` char(128),"
			"PRIMARY KEY(`userID`),"
			"UNIQUE(`username`)"
			") ENGINE=InnoDB",

			"CREATE TABLE `Items` ("
			"`itemID` int(11) NOT NULL AUTO_INCREMENT,"
			"`brand` char(40) NOT NULL,"
			"`model` char(40),"
			"PRIMARY KEY(`itemID`)"
			") ENGINE=InnoDB",

			"CREATE TABLE `Companies` ("
			"`companyID` int(11) NOT NULL AUTO_INCREMENT,"
			"`companyName` char(40) NOT NULL,"
			"`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
			"PRIMARY KEY(`companyID`),"
			"UNIQUE(`companyName`)"
			") ENGINE=InnoDB",

			"CREATE TABLE `Locations` ("
			"`locationID` int(11) NOT NULL AUTO_INCREMENT,"
			"`streetAddress` char(240),"
			"`city` char(40) NOT NULL,"
			"`state` char(2) NOT NULL,"
			"`zip` int(11),"
			"`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
			"PRIMARY KEY(`locationID`)"
			") ENGINE=InnoDB",

			"CREATE TABLE `CompanyLocationMap` ("
			"`clmapID` int(11) NOT NULL AUTO_INCREMENT,"	
			"`companyID` int(11) NOT NULL,"
			"`locationID` int(11) NOT NULL,"
			"PRIMARY KEY(`clmapID`),"
			"FOREIGN KEY(`companyID`) REFERENCES `Companies` (`companyID`) ON DELETE NO ACTION,"
			"FOREIGN KEY(`locationID`) REFERENCES `Locations` (`locationID`) ON DELETE NO ACTION"
			") ENGINE=InnoDB",

			"CREATE TABLE `ItemMap` ("
			"`itemMapID` int(11) NOT NULL AUTO_INCREMENT,"
			"`clmapID` int(11) NOT NULL,"
			"`itemID` int(11) NOT NULL,"
			"`userID` int(11) NOT NULL,"
			"`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
			"PRIMARY KEY(`itemMapID`),"
			"FOREIGN KEY(`clmapID`) REFERENCES `CompanyLocationMap` (`clmapID`) ON DELETE NO ACTION,"
			"FOREIGN KEY(`itemID`) REFERENCES `Items` (`itemID`) ON DELETE NO ACTION,"
			"FOREIGN KEY(`userID`) REFERENCES `Users` (`userID`) ON DELETE NO ACTION"
			") ENGINE=InnoDB",
			]

		for ddl in TABLES:
			self.cur.execute(ddl)
