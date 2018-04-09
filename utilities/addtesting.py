import requests
import datetime
import json

def sendPostRequest(token, brand, model, company, address, city, state, zipCode):
	API_ENDPOINT = "https://itemeyes-199123.appspot.com/add"

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
	for i in range(1, 10001):
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

