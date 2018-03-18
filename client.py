import requests

URL = 'https://lovefrompenelope.herokuapp.com/'

data = requests.get(URL)
print(data)
print('Response from server: ')
print(data.text)
