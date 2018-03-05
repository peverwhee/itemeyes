from dbcreator import CreateDB
from dbdata import *
from dbproxy import dbProxy


def main():
	create = CreateDB()
	host = "localhost"
	proxy = dbProxy(host)

	#add new user
	newUser = User("courtney", "peverley", "cmpeverley")
	proxy.addUser(newUser)

	#add new company
	newCompany = Company("JC Penney")
	proxy.addCompany(newCompany)
	print(newCompany.companyID)

	#add new location (and also a map to the company)
	newLocation = Location("761 Lawson Ave", "Erie", "CO", 80516, newCompany.companyID)
	mapID = proxy.addLocation(newLocation)

	#add new item (and also a map to the user who added it, and the company/location)
	newItem = Item("Neutrogena", "makeup removing wipes", newUser.userID, mapID)
	proxy.addItem(newItem)

if __name__ == '__main__':
	main()