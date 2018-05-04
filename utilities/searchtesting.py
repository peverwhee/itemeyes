import requests
import json
import datetime

def sendPostRequest(token, brand, model, zipCode):
	# for app engine:
	#API_ENDPOINT = "https://itemeyes-199123.appspot.com/search"
	# for kubernetes:
	#API_ENDPOINT = "http://35.193.33.30/search"
	# for compute:
	API_ENDPOINT = "http://35.185.19.16/search"

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
		sendPostRequest(token, brand, model, zipCode)
	print("end time is:")
	print(datetime.datetime.now().time())


if __name__ == '__main__':
	main()

