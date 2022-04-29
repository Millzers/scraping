import json

prices = []

#file = "r'C:\Users\Logan\PycharmProjects\scraping\psa_alakazam_10.json'"

with open('psa_alakazam_10.json', 'r') as json_file:
	json_load = json.load(json_file)

json_load
for x in json_load:
	prices = float(x['PRICE'].lstrip("$"))
	print(prices)