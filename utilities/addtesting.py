import requests
import datetime
import json

def sendPostRequest(token, brand, model, company, address, city, state, zipCode):
	# for app engine:
	#API_ENDPOINT = "https://itemeyes-199123.appspot.com/add"
	# for kubernetes:
	API_ENDPOINT = "http://35.193.33.30/add"
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

def main():
	print("start time is:")
	print(datetime.datetime.now().time())
	state = 'CA'
	zipCode = 12345
	token = "1234xyz"
	for i in range(10001, 12251):
		brand = 'brand' + `i`
		model = 'model' + `i`
		company = 'company' + `i`
		address = 'address' + `i`
		city = 'city' + `i`
		sendPostRequest(token, brand, model, company, address, city, state, zipCode)

	print("end time is:")
	print(datetime.datetime.now().time())

if __name__ == '__main__':
	main()

