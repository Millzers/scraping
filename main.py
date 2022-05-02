import json

def get_prices():
    prices = 0
    i = 0 #iterator
    # open the .json file that contains the PSA data for the card.
    with open('psa_alakazam_9.json' , 'r') as json_file:
        json_load = json.load(json_file)

    for x in json_load[1:]: # for every dictionary in json_load
        prices += float(x['PRICE'].lstrip("$"))  # get the values with the 'PRICES' key

    most_recent = json_load[1]  # get the most recent sale
    print(most_recent)
    fresh_price = float(most_recent['PRICE'].lstrip("$").replace(',',''))  # get the price for the most recent sale
    print('fresh price :' , fresh_price)
    avg_price = (prices + fresh_price)/6  # get the average price. Most recent sale is included twice in the formula.
    print('avg :', avg_price)
    fair_price = "${:,.2f}".format(avg_price * .95)  # 95% of the average price is a fair price.
    good_price = "${:,.2f}".format(avg_price * .85)  # 85% of the average price is a good price.
    great_price = "${:,.2f}".format(avg_price * .75)  # 75% of the average price is a great price.

    keys = ["FAIR PRICE", "GOOD PRICE", "GREAT PRICE"]
    values = [fair_price, good_price, great_price]
    data = (dict(zip(keys, values)))
    print(data)
    return data

get_prices()