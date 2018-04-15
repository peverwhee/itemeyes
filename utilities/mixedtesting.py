import requests
import json
import datetime

def sendPostRequestAdd(token, brand, model, company, address, city, state, zipCode):
	# for app engine:
	API_ENDPOINT = "https://itemeyes-199123.appspot.com/add"
	# for kubernetes:
	#API_ENDPOINT = "http://35.193.33.30/add"
	# for compute:
	#API_ENDPOINT = "http://35.185.19.16/add"

	data = {'brand': brand,
			'model': model,
			'company': company,
			'address': address,
			'city': city,
			'state': state,
			'zip': zipCode,
			'token': token,
			}

	r = requests.post(url=API_ENDPOINT, data=json.dumps(data))

	jsonText = r.text
	#print(r.text)
	jsonObject = json.loads(jsonText)

def sendPostRequestSearch(token, brand, model, zipCode):
	API_ENDPOINT = "https://itemeyes-199123.appspot.com/search"

	data = {'brand': brand,
			'model': model,
			'zip': zipCode,
			'token': token,
			}

	r = requests.post(url=API_ENDPOINT, data=json.dumps(data))

	jsonText = r.text
	print(r.text)
	jsonObject = json.loads(jsonText)

def main():
	state = 'CA'
	zipCode = 12345
	token = "1234xyz"
	print("start time is:")
	print(datetime.datetime.now().time())
	for i in range(114, 124):
		brand = 'brand' + `i`
		model = 'model' + `i`
		company = 'company' + `i`
		address = 'address' + `i`
		city = 'city' + `i`
		sendPostRequestAdd(token, brand, model, company, address, city, state, zipCode)
		sendPostRequestSearch(token, brand, model, zipCode)
		sendPostRequestSearch(token, brand, model, zipCode)
		sendPostRequestSearch(token, brand, model, zipCode)
		sendPostRequestSearch(token, brand, model, zipCode)
		sendPostRequestSearch(token, brand, model, zipCode)
	print("end time is:")
	print(datetime.datetime.now().time())


if __name__ == '__main__':
	main()

