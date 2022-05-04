# scraping
# Developed by Logan Miller
# Last updated 5/1/2022
from telnetlib import EC

import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Problems
# 1. How to get "pokemon" to show up without foreign characters
# 2.

headers = ['Auction URL', 'Auction Title', 'Current Bid Price', 'Number of Bids', 'Time Left on Auction',
           'Link to Image of Auction']
ebay_table_headers = ['Auction Image', 'Auction Title', 'Current Bid Price', 'Number of Bids', 'Time Left on Auction']
psa_table_headers = ['Date', 'Price', 'Grade', 'Lot #', 'Auction House', 'Seller', 'Type', 'Cert']
psa_table_header_keys = ['header1', 'header2', 'header3', 'header4', 'header5', 'header6']


# This function finds the number of "exact" search results on the eBay page. eBay shows a number of additional search
# results that are similar to what you searched for underneath the actual search results. We use the resulting number
# of this function and plug it into the scraper to only gather the first X results.
# def numOfResults(url):
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, "html5lib")
#     x = soup.find_all("h1", class_="rsHdr")[  # srp-controls__count-heading // tag for regular search page
#         0
#     ].text  # find the number of search results line on the web page and store it in 'x' variable
#     numOfResults = int(
#         x.split()[0]
#     )  # read the first word(actually an integer) from the number of search results string into the 'numOfResults'
#     # variable, and parse into an int
#     return numOfResults


def convert_to_json(data, file):
    with open(file, 'w') as f:
        f.write(json.dumps(data, indent=2))

    results_read_from_file = None
    with open(file, 'r') as f:
        data_as_string = f.read()
        print(data_as_string)
        results_read_from_file = json.loads(data_as_string)

    print('Loaded from file:')
    print(results_read_from_file)


def getMarketPrice(url):  # scrape psa website for the table
    i = 0
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "td")))
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "th")))
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#itemResults")))
    except: print("Driver Timed Out.")

    table = driver.find_elements(by=By.CSS_SELECTOR, value="#itemResults")[0]
    headers = [header.text for header in table.find_elements(by=By.TAG_NAME, value='th') if header.text != '']
    rows = table.find_elements(by=By.TAG_NAME, value='tbody')[0].find_elements(by=By.TAG_NAME, value='tr')

    results = []
    results.append(dict(zip(psa_table_headers, psa_table_headers)))
    for row in rows:
        if i < 5:
            values = [element.text for element in row.find_elements(by=By.TAG_NAME, value='td') if element.text != '']
            print(values)
            results.append(dict(zip(headers, values)))
            i += 1
    print("results = ", results)
    return results


def html_format(card_data, card_data_list, title, price, number_of_bids, time_left, auction_link, image):
    card_data_list.append(dict(zip(headers, ebay_table_headers)))
    html_image = (
                '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')
    card_data.extend([html_image])
    card_data.extend([title])
    card_data.extend([price])
    card_data.extend([number_of_bids])
    card_data.extend([time_left])


def get_prices(file):
    prices = 0
    i = 0 #iterator
    # open the .json file that contains the PSA data for the card.
    with open(file, 'r') as json_file:
        json_load = json.load(json_file)

    for x in json_load[1:]: # for every dictionary in json_load
        prices += float(x['PRICE'].lstrip("$").replace(',',''))  # get the values with the 'PRICES' key


    most_recent = json_load[1]  # get the most recent sale
    fresh_price = float(most_recent['PRICE'].lstrip("$").replace(',',''))  # get the price for the most recent sale
    avg_price = (prices + fresh_price) / 6  # get the average price. Most recent sale is included twice in the formula.
    fair_price = "${:,.2f}".format(avg_price * .95)  # 95% of the average price is a fair price.
    good_price = "${:,.2f}".format(avg_price * .85)  # 85% of the average price is a good price.
    great_price = "${:,.2f}".format(avg_price * .75)  # 75% of the average price is a great price.

    keys = ["FAIR PRICE", "GOOD PRICE", "GREAT PRICE"]
    values = [fair_price, good_price, great_price]
    data = (dict(zip(keys, values)))
    return data


############################################### SCRAPING ALAKAZAM ######################################################

def alakazam_10():
    print("Alakazam 10's")
    ebay_file = "ebay_alakazam_10.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_10.json"  # json file name that will contain psa data
    price_file = "prices_alakazam_10.json"  # json file name that will contain price data ########################
    # url for eBay auction
    #### TEST URL #####
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"7"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544021#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # list that will contain the dictionaries of card data after they are zipped

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) for eBay tables


    for card in cards:  # Scrape search results for the following data from ebay

        card_data = []  # list to append scraped data to
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate
        # the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file
    price_results = get_prices(psa_file)  # get_prices() takes the prices from the psa files and manipulates them.
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

def alakazam_9pt5():
    print("Alakazam 9.5's")
    ebay_file = "ebay_alakazam_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_alakazam_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"9.5"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+10%2C+8%2C+7%2C+9%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544021#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay

        card_data = []  # list to append scraped data to
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def alakazam_9():
    print("Alakazam 9's")
    ebay_file = "ebay_alakazam_9.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_9.json"  # json file name that will contain psa data
    price_file = 'prices_alakazam_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"9"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+10%2C+8%2C+7%2C+9.5%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544021#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def alakazam_8pt5():
    print("Alakazam 8.5's")
    ebay_file = "ebay_alakazam_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_alakazam_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"10"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+9%2C+8%2C+7%2C+9.5%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544021#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def alakazam_8():
    print("Alakazam 8's")
    ebay_file = "ebay_alakazam_8.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_8.json"  # json file name that will contain psa data
    price_file = 'prices_alakazam_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"8"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+8.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544021#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def alakazam_7pt5():
    print("Alakazam 7.5's")
    ebay_file = "ebay_alakazam_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_alakazam_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"7.5"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+8.5+8+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544021#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def alakazam_7():
    print("Alakazam 7's")
    ebay_file = "ebay_alakazam_7.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_7.json"  # json file name that will contain psa data
    price_file = 'prices_alakazam_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"7"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+8.5+8+7.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544021#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        print(card_data)

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

    ######################################## SCRAPING BLASTOISE#########################################################

def blastoise_10():
    print("blastoise 10's")
    ebay_file = "ebay_blastoise_10.json"  # json file name that will contain eBay data
    psa_file = "psa_blastoise_10.json"  # json file name that will contain psa data
    price_file = "prices_blastoise_10.json"  # json file name that will contain price data ########################
    # url for eBay auction
    #### TEST URL #####
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="blastoise"+"2%2F102"+"10"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+9.5%2C+8%2C+7%2C+9%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/blastoise-holo/values/544023#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # list that will contain the dictionaries of card data after they are zipped

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) for eBay tables


    for card in cards:  # Scrape search results for the following data from ebay

        card_data = []  # list to append scraped data to
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate
        # the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file
    price_results = get_prices(psa_file)  # get_prices() takes the prices from the psa files and manipulates them.
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

def blastoise_9pt5():
    print("blastoise 9.5's")
    ebay_file = "ebay_blastoise_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_blastoise_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_blastoise_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="blastoise"+"2%2F102"+"9.5"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+10%2C+8%2C+7%2C+9%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/blastoise-holo/values/544023#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay

        card_data = []  # list to append scraped data to
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def blastoise_9():
    print("blastoise 9's")
    ebay_file = "ebay_blastoise_9.json"  # json file name that will contain eBay data
    psa_file = "psa_blastoise_9.json"  # json file name that will contain psa data
    price_file = 'prices_blastoise_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="blastoise"+"2%2F102"+"9"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+10%2C+9.5%2C+8%2C+7%2C+8.5%2C+7.57.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/blastoise-holo/values/544023#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def blastoise_8pt5():
    print("blastoise 8.5's")
    ebay_file = "ebay_blastoise_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_blastoise_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_blastoise_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="blastoise"+"2%2F102"+"8.5"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+10%2C+9%2C+9.5%2C+8%2C+7%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/blastoise-holo/values/544023#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def blastoise_8():
    print("blastoise 8's")
    ebay_file = "ebay_blastoise_8.json"  # json file name that will contain eBay data
    psa_file = "psa_blastoise_8.json"  # json file name that will contain psa data
    price_file = 'prices_blastoise_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="blastoise"+"2%2F102"+"8"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+8.5%2C+10%2C+9%2C+9.5%2C+7%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/blastoise-holo/values/544023#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def blastoise_7pt5():
    print("blastoise 7.5's")
    ebay_file = "ebay_blastoise_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_blastoise_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_blastoise_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="blastoise"+"2%2F102"+"7.5"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+8.5%2C+10%2C+9%2C+9.5%2C+7%2C+8&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/blastoise-holo/values/544023#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def blastoise_7():
    print("blastoise 7's")
    ebay_file = "ebay_blastoise_7.json"  # json file name that will contain eBay data
    psa_file = "psa_blastoise_7.json"  # json file name that will contain psa data
    price_file = 'prices_blastoise_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="blastoise"+"2%2F102"+"7"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+7.5%2C+8.5%2C+10%2C+9%2C+9.5%2C+8&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/blastoise-holo/values/544023#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        print(card_data)

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING chansey #######################################################

def chansey_10():
    print("chansey 10's")
    ebay_file = "ebay_chansey_10.json"  # json file name that will contain eBay data
    psa_file = "psa_chansey_10.json"  # json file name that will contain psa data
    price_file = "prices_chansey_10.json"  # json file name that will contain price data ########################
    # url for eBay auction
    #### TEST URL #####
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="chansey"+"3%2F102"+"10"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+9.5%2C+9%2C+8.5%2C+8%2C+7.5%2C+7&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/chansey-holo/values/544025#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # list that will contain the dictionaries of card data after they are zipped

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) for eBay tables


    for card in cards:  # Scrape search results for the following data from ebay

        card_data = []  # list to append scraped data to
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate
        # the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file
    price_results = get_prices(psa_file)  # get_prices() takes the prices from the psa files and manipulates them.
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

def chansey_9pt5():
    print("chansey 9.5's")
    ebay_file = "ebay_chansey_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_chansey_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_chansey_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="chansey"+"3%2F102"+"9.5"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+10%2C+9%2C+8.5%2C+8%2C+7.5%2C+7&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/chansey-holo/values/544025#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay

        card_data = []  # list to append scraped data to
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def chansey_9():
    print("chansey 9's")
    ebay_file = "ebay_chansey_9.json"  # json file name that will contain eBay data
    psa_file = "psa_chansey_9.json"  # json file name that will contain psa data
    price_file = 'prices_chansey_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="chansey"+"3%2F102"+"9"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+10%2C+9.5%2C+8.5%2C+8%2C+7.5%2C+7&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/chansey-holo/values/544025#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def chansey_8pt5():
    print("chansey 8.5's")
    ebay_file = "ebay_chansey_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_chansey_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_chansey_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="chansey"+"3%2F102"+"8.5"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+10%2C+9%2C+9.5%2C+8%2C+7%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/chansey-holo/values/544025#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def chansey_8():
    print("chansey 8's")
    ebay_file = "ebay_chansey_8.json"  # json file name that will contain eBay data
    psa_file = "psa_chansey_8.json"  # json file name that will contain psa data
    price_file = 'prices_chansey_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="chansey"+"3%2F102"+"8"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+8.5%2C+10%2C+9%2C+9.5%2C+7%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/chansey-holo/values/544025#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def chansey_7pt5():
    print("chansey 7.5's")
    ebay_file = "ebay_chansey_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_chansey_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_chansey_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="chansey"+"3%2F102"+"7.5"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+8.5%2C+10%2C+9%2C+9.5%2C+7%2C+8&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/chansey-holo/values/544025#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def chansey_7():
    print("chansey 7's")
    ebay_file = "ebay_chansey_7.json"  # json file name that will contain eBay data
    psa_file = "psa_chansey_7.json"  # json file name that will contain psa data
    price_file = 'prices_chansey_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="chansey"+"3%2F102"+"10"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+anniversary%2C+celebrations%2C+9.5%2C+9%2C+8.5%2C+8%2C+7.5%2C+7&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/chansey-holo/values/544025#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        print(card_data)

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


############################################### SCRAPING CHARIZARD #####################################################

def charizard_10():
    print("Charizard 10's")
    ebay_file = "ebay_charizard_10.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_10.json"  # json file name that will contain psa data
    price_file = 'prices_charizard_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+8+7.5+7+lot+damaged+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/charizard-holo/values/544027#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def charizard_9pt5():
    print("Charizard 9.5's")
    ebay_file = "ebay_charizard_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_charizard_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544027#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def charizard_9():
    print("Charizard 9's")
    ebay_file = "ebay_charizard_9.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_9.json"  # json file name that will contain psa data
    price_file = 'prices_charizard_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544027#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def charizard_8pt5():
    print("Charizard 8.5's")
    ebay_file = "ebay_charizard_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_charizard_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544027#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def charizard_8():
    print("Charizard 8's")
    ebay_file = "ebay_charizard_8.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_8.json"  # json file name that will contain psa data
    price_file = 'prices_charizard_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544027#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def charizard_7pt5():
    print("Charizard 7.5's")
    ebay_file = "ebay_charizard_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_charizard_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544027#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def charizard_7():
    print("Charizard 7's")
    ebay_file = "ebay_charizard_7.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_7.json"  # json file name that will contain psa data
    price_file = 'prices_charizard_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544027#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING CLEFAIRY #####################################################

def clefairy_10():
    print("clefairy 10's")
    ebay_file = "ebay_clefairy_10.json"  # json file name that will contain eBay data
    psa_file = "psa_clefairy_10.json"  # json file name that will contain psa data
    price_file = 'prices_clefairy_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="clefairy"+"5%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544029#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def clefairy_9pt5():
    print("clefairy 9.5's")
    ebay_file = "ebay_clefairy_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_clefairy_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_clefairy_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="clefairy"+"5%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544029#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def clefairy_9():
    print("clefairy 9's")
    ebay_file = "ebay_clefairy_9.json"  # json file name that will contain eBay data
    psa_file = "psa_clefairy_9.json"  # json file name that will contain psa data
    price_file = 'prices_clefairy_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="clefairy"+"5%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544029#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def clefairy_8pt5():
    print("clefairy 8.5's")
    ebay_file = "ebay_clefairy_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_clefairy_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_clefairy_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="clefairy"+"5%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544029#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def clefairy_8():
    print("clefairy 8's")
    ebay_file = "ebay_clefairy_8.json"  # json file name that will contain eBay data
    psa_file = "psa_clefairy_8.json"  # json file name that will contain psa data
    price_file = 'prices_clefairy_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="clefairy"+"5%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544029#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def clefairy_7pt5():
    print("clefairy 7.5's")
    ebay_file = "ebay_clefairy_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_clefairy_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_clefairy_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="clefairy"+"5%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544029#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def clefairy_7():
    print("clefairy 7's")
    ebay_file = "ebay_clefairy_7.json"  # json file name that will contain eBay data
    psa_file = "psa_clefairy_7.json"  # json file name that will contain psa data
    price_file = 'prices_clefairy_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="clefairy"+"5%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544029#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING GYARADOS #####################################################

def gyarados_10():
    print("gyarados 10's")
    ebay_file = "ebay_gyarados_10.json"  # json file name that will contain eBay data
    psa_file = "psa_gyarados_10.json"  # json file name that will contain psa data
    price_file = 'prices_gyarados_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="gyarados"+"6%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/gyarados-holo/values/544031#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def gyarados_9pt5():
    print("gyarados 9.5's")
    ebay_file = "ebay_gyarados_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_gyarados_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_gyarados_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="gyarados"+"6%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544031#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def gyarados_9():
    print("gyarados 9's")
    ebay_file = "ebay_gyarados_9.json"  # json file name that will contain eBay data
    psa_file = "psa_gyarados_9.json"  # json file name that will contain psa data
    price_file = 'prices_gyarados_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="gyarados"+"6%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544031#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def gyarados_8pt5():
    print("gyarados 8.5's")
    ebay_file = "ebay_gyarados_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_gyarados_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_gyarados_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="gyarados"+"6%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544031#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def gyarados_8():
    print("gyarados 8's")
    ebay_file = "ebay_gyarados_8.json"  # json file name that will contain eBay data
    psa_file = "psa_gyarados_8.json"  # json file name that will contain psa data
    price_file = 'prices_gyarados_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="gyarados"+"6%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544031#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def gyarados_7pt5():
    print("gyarados 7.5's")
    ebay_file = "ebay_gyarados_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_gyarados_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_gyarados_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="gyarados"+"6%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544031#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def gyarados_7():
    print("gyarados 7's")
    ebay_file = "ebay_gyarados_7.json"  # json file name that will contain eBay data
    psa_file = "psa_gyarados_7.json"  # json file name that will contain psa data
    price_file = 'prices_gyarados_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="gyarados"+"6%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544031#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING HITMONCHAN #########################################################################################################################################

def hitmonchan_10():
    print("hitmonchan 10's")
    ebay_file = "ebay_hitmonchan_10.json"  # json file name that will contain eBay data
    psa_file = "psa_hitmonchan_10.json"  # json file name that will contain psa data
    price_file = 'prices_hitmonchan_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="hitmonchan"+"7%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544033#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def hitmonchan_9pt5():
    print("hitmonchan 9.5's")
    ebay_file = "ebay_hitmonchan_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_hitmonchan_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_hitmonchan_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="hitmonchan"+"7%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544033#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def hitmonchan_9():
    print("hitmonchan 9's")
    ebay_file = "ebay_hitmonchan_9.json"  # json file name that will contain eBay data
    psa_file = "psa_hitmonchan_9.json"  # json file name that will contain psa data
    price_file = 'prices_hitmonchan_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="hitmonchan"+"7%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544033#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def hitmonchan_8pt5():
    print("hitmonchan 8.5's")
    ebay_file = "ebay_hitmonchan_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_hitmonchan_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_hitmonchan_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="hitmonchan"+"7%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544033#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def hitmonchan_8():
    print("hitmonchan 8's")
    ebay_file = "ebay_hitmonchan_8.json"  # json file name that will contain eBay data
    psa_file = "psa_hitmonchan_8.json"  # json file name that will contain psa data
    price_file = 'prices_hitmonchan_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="hitmonchan"+"7%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544033#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def hitmonchan_7pt5():
    print("hitmonchan 7.5's")
    ebay_file = "ebay_hitmonchan_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_hitmonchan_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_hitmonchan_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="hitmonchan"+"7%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544033#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def hitmonchan_7():
    print("hitmonchan 7's")
    ebay_file = "ebay_hitmonchan_7.json"  # json file name that will contain eBay data
    psa_file = "psa_hitmonchan_7.json"  # json file name that will contain psa data
    price_file = 'prices_hitmonchan_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="hitmonchan"+"7%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544033#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING MAGNETON #####################################################

def magneton_10():
    print("magneton 10's")
    ebay_file = "ebay_magneton_10.json"  # json file name that will contain eBay data
    psa_file = "psa_magneton_10.json"  # json file name that will contain psa data
    price_file = 'prices_magneton_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="magneton"+"9%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9.5+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544037#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def magneton_9pt5():
    print("magneton 9.5's")
    ebay_file = "ebay_magneton_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_magneton_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_magneton_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="magneton"+"9%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544037#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def magneton_9():
    print("magneton 9's")
    ebay_file = "ebay_magneton_9.json"  # json file name that will contain eBay data
    psa_file = "psa_magneton_9.json"  # json file name that will contain psa data
    price_file = 'prices_magneton_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="magneton"+"9%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544037#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def magneton_8pt5():
    print("magneton 8.5's")
    ebay_file = "ebay_magneton_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_magneton_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_magneton_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="magneton"+"9%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544037#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def magneton_8():
    print("magneton 8's")
    ebay_file = "ebay_magneton_8.json"  # json file name that will contain eBay data
    psa_file = "psa_magneton_8.json"  # json file name that will contain psa data
    price_file = 'prices_magneton_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="magneton"+"9%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544037#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def magneton_7pt5():
    print("magneton 7.5's")
    ebay_file = "ebay_magneton_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_magneton_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_magneton_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="magneton"+"9%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544037#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def magneton_7():
    print("magneton 7's")
    ebay_file = "ebay_magneton_7.json"  # json file name that will contain eBay data
    psa_file = "psa_magneton_7.json"  # json file name that will contain psa data
    price_file = 'prices_magneton_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="magneton"+"9%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544037#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING MEWTWO #####################################################

def mewtwo_10():
    print("mewtwo 10's")
    ebay_file = "ebay_mewtwo_10.json"  # json file name that will contain eBay data
    psa_file = "psa_mewtwo_10.json"  # json file name that will contain psa data
    price_file = 'prices_mewtwo_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="mewtwo"+"10%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544039#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def mewtwo_9pt5():
    print("mewtwo 9.5's")
    ebay_file = "ebay_mewtwo_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_mewtwo_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_mewtwo_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="mewtwo"+"10%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544039#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def mewtwo_9():
    print("mewtwo 9's")
    ebay_file = "ebay_mewtwo_9.json"  # json file name that will contain eBay data
    psa_file = "psa_mewtwo_9.json"  # json file name that will contain psa data
    price_file = 'prices_mewtwo_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="mewtwo"+"10%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544039#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def mewtwo_8pt5():
    print("mewtwo 8.5's")
    ebay_file = "ebay_mewtwo_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_mewtwo_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_mewtwo_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="mewtwo"+"10%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544039#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def mewtwo_8():
    print("mewtwo 8's")
    ebay_file = "ebay_mewtwo_8.json"  # json file name that will contain eBay data
    psa_file = "psa_mewtwo_8.json"  # json file name that will contain psa data
    price_file = 'prices_mewtwo_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="mewtwo"+"10%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544039#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def mewtwo_7pt5():
    print("mewtwo 7.5's")
    ebay_file = "ebay_mewtwo_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_mewtwo_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_mewtwo_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="mewtwo"+"10%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544039#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def mewtwo_7():
    print("mewtwo 7's")
    ebay_file = "ebay_mewtwo_7.json"  # json file name that will contain eBay data
    psa_file = "psa_mewtwo_7.json"  # json file name that will contain psa data
    price_file = 'prices_mewtwo_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="mewtwo"+"10%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544039#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING NIDOKING #####################################################

def nidoking_10():
    print("nidoking 10's")
    ebay_file = "ebay_nidoking_10.json"  # json file name that will contain eBay data
    psa_file = "psa_nidoking_10.json"  # json file name that will contain psa data
    price_file = 'prices_nidoking_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="nidoking"+11%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544041#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def nidoking_9pt5():
    print("nidoking 9.5's")
    ebay_file = "ebay_nidoking_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_nidoking_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_nidoking_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="nidoking"+11%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544041#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def nidoking_9():
    print("nidoking 9's")
    ebay_file = "ebay_nidoking_9.json"  # json file name that will contain eBay data
    psa_file = "psa_nidoking_9.json"  # json file name that will contain psa data
    price_file = 'prices_nidoking_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="nidoking"+"11%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544041#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def nidoking_8pt5():
    print("nidoking 8.5's")
    ebay_file = "ebay_nidoking_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_nidoking_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_nidoking_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="nidoking"+"11%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544041#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def nidoking_8():
    print("nidoking 8's")
    ebay_file = "ebay_nidoking_8.json"  # json file name that will contain eBay data
    psa_file = "psa_nidoking_8.json"  # json file name that will contain psa data
    price_file = 'prices_nidoking_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="nidoking"+"11%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544041#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def nidoking_7pt5():
    print("nidoking 7.5's")
    ebay_file = "ebay_nidoking_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_nidoking_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_nidoking_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="nidoking"+"11%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544041#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def nidoking_7():
    print("nidoking 7's")
    ebay_file = "ebay_nidoking_7.json"  # json file name that will contain eBay data
    psa_file = "psa_nidoking_7.json"  # json file name that will contain psa data
    price_file = 'prices_nidoking_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="nidoking"+"11%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544041#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING NINETALES #####################################################

def ninetales_10():
    print("ninetales 10's")
    ebay_file = "ebay_ninetales_10.json"  # json file name that will contain eBay data
    psa_file = "psa_ninetales_10.json"  # json file name that will contain psa data
    price_file = 'prices_ninetales_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="ninetales"+"12%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544043#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def ninetales_9pt5():
    print("ninetales 9.5's")
    ebay_file = "ebay_ninetales_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_ninetales_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_ninetales_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="ninetales"+"12%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544043#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def ninetales_9():
    print("ninetales 9's")
    ebay_file = "ebay_ninetales_9.json"  # json file name that will contain eBay data
    psa_file = "psa_ninetales_9.json"  # json file name that will contain psa data
    price_file = 'prices_ninetales_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="ninetales"+"12%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544043#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def ninetales_8pt5():
    print("ninetales 8.5's")
    ebay_file = "ebay_ninetales_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_ninetales_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_ninetales_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="ninetales"+"12%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544043#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def ninetales_8():
    print("ninetales 8's")
    ebay_file = "ebay_ninetales_8.json"  # json file name that will contain eBay data
    psa_file = "psa_ninetales_8.json"  # json file name that will contain psa data
    price_file = 'prices_ninetales_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="ninetales"+"12%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544043#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def ninetales_7pt5():
    print("ninetales 7.5's")
    ebay_file = "ebay_ninetales_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_ninetales_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_ninetales_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="ninetales"+"12%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544043#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def ninetales_7():
    print("ninetales 7's")
    ebay_file = "ebay_ninetales_7.json"  # json file name that will contain eBay data
    psa_file = "psa_ninetales_7.json"  # json file name that will contain psa data
    price_file = 'prices_ninetales_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="ninetales"+"12%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544043#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING POLIWRATH #####################################################

def poliwrath_10():
    print("poliwrath 10's")
    ebay_file = "ebay_poliwrath_10.json"  # json file name that will contain eBay data
    psa_file = "psa_poliwrath_10.json"  # json file name that will contain psa data
    price_file = 'prices_poliwrath_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="poliwrath"+"13%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544045#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def poliwrath_9pt5():
    print("poliwrath 9.5's")
    ebay_file = "ebay_poliwrath_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_poliwrath_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_poliwrath_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="poliwrath"+"13%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544045#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def poliwrath_9():
    print("poliwrath 9's")
    ebay_file = "ebay_poliwrath_9.json"  # json file name that will contain eBay data
    psa_file = "psa_poliwrath_9.json"  # json file name that will contain psa data
    price_file = 'prices_poliwrath_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="poliwrath"+"13%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544045#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def poliwrath_8pt5():
    print("poliwrath 8.5's")
    ebay_file = "ebay_poliwrath_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_poliwrath_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_poliwrath_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="poliwrath"+"13%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544045#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def poliwrath_8():
    print("poliwrath 8's")
    ebay_file = "ebay_poliwrath_8.json"  # json file name that will contain eBay data
    psa_file = "psa_poliwrath_8.json"  # json file name that will contain psa data
    price_file = 'prices_poliwrath_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="poliwrath"+"13%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544045#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def poliwrath_7pt5():
    print("poliwrath 7.5's")
    ebay_file = "ebay_poliwrath_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_poliwrath_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_poliwrath_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="poliwrath"+"13%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544045#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def poliwrath_7():
    print("poliwrath 7's")
    ebay_file = "ebay_poliwrath_7.json"  # json file name that will contain eBay data
    psa_file = "psa_poliwrath_7.json"  # json file name that will contain psa data
    price_file = 'prices_poliwrath_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="poliwrath"+"13%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544045#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING RAICHU #####################################################

def raichu_10():
    print("raichu 10's")
    ebay_file = "ebay_raichu_10.json"  # json file name that will contain eBay data
    psa_file = "psa_raichu_10.json"  # json file name that will contain psa data
    price_file = 'prices_raichu_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="raichu"+"14%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544047#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def raichu_9pt5():
    print("raichu 9.5's")
    ebay_file = "ebay_raichu_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_raichu_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_raichu_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="raichu"+"14%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544047#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def raichu_9():
    print("raichu 9's")
    ebay_file = "ebay_raichu_9.json"  # json file name that will contain eBay data
    psa_file = "psa_raichu_9.json"  # json file name that will contain psa data
    price_file = 'prices_raichu_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="raichu"+"14%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544047#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def raichu_8pt5():
    print("raichu 8.5's")
    ebay_file = "ebay_raichu_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_raichu_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_raichu_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="raichu"+"14%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544047#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def raichu_8():
    print("raichu 8's")
    ebay_file = "ebay_raichu_8.json"  # json file name that will contain eBay data
    psa_file = "psa_raichu_8.json"  # json file name that will contain psa data
    price_file = 'prices_raichu_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="raichu"+"14%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544047#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def raichu_7pt5():
    print("raichu 7.5's")
    ebay_file = "ebay_raichu_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_raichu_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_raichu_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="raichu"+"14%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544047#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def raichu_7():
    print("raichu 7's")
    ebay_file = "ebay_raichu_7.json"  # json file name that will contain eBay data
    psa_file = "psa_raichu_7.json"  # json file name that will contain psa data
    price_file = 'prices_raichu_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="raichu"+"14%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544047#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING VENUSAUR #####################################################

def venusaur_10():
    print("venusaur 10's")
    ebay_file = "ebay_venusaur_10.json"  # json file name that will contain eBay data
    psa_file = "psa_venusaur_10.json"  # json file name that will contain psa data
    price_file = 'prices_venusaur_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="venusaur"+"15%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544049#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def venusaur_9pt5():
    print("venusaur 9.5's")
    ebay_file = "ebay_venusaur_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_venusaur_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_venusaur_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="venusaur"+"15%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544049#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def venusaur_9():
    print("venusaur 9's")
    ebay_file = "ebay_venusaur_9.json"  # json file name that will contain eBay data
    psa_file = "psa_venusaur_9.json"  # json file name that will contain psa data
    price_file = 'prices_venusaur_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="venusaur"+"15%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544049#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def venusaur_8pt5():
    print("venusaur 8.5's")
    ebay_file = "ebay_venusaur_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_venusaur_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_venusaur_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="venusaur"+"15%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544049#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def venusaur_8():
    print("venusaur 8's")
    ebay_file = "ebay_venusaur_8.json"  # json file name that will contain eBay data
    psa_file = "psa_venusaur_8.json"  # json file name that will contain psa data
    price_file = 'prices_venusaur_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="venusaur"+"15%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544049#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def venusaur_7pt5():
    print("venusaur 7.5's")
    ebay_file = "ebay_venusaur_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_venusaur_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_venusaur_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="venusaur"+"15%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544049#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def venusaur_7():
    print("venusaur 7's")
    ebay_file = "ebay_venusaur_7.json"  # json file name that will contain eBay data
    psa_file = "psa_venusaur_7.json"  # json file name that will contain psa data
    price_file = 'prices_venusaur_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="venusaur"+"15%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544049#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.

############################################### SCRAPING ZAPDOS #####################################################

def zapdos_10():
    print("zapdos 10's")
    ebay_file = "ebay_zapdos_10.json"  # json file name that will contain eBay data
    psa_file = "psa_zapdos_10.json"  # json file name that will contain psa data
    price_file = 'prices_zapdos_10.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="zapdos"+"16%2F102"++"10"&_in_kw=1&_ex_kw=celebrations+1st+9+9.5+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544051#g=10'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def zapdos_9pt5():
    print("zapdos 9.5's")
    ebay_file = "ebay_zapdos_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_zapdos_9pt5.json"  # json file name that will contain psa data
    price_file = 'prices_zapdos_9pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="zapdos"+"16%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+1st+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544051#g=9.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def zapdos_9():
    print("zapdos 9's")
    ebay_file = "ebay_zapdos_9.json"  # json file name that will contain eBay data
    psa_file = "psa_zapdos_9.json"  # json file name that will contain psa data
    price_file = 'prices_zapdos_9.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="zapdos"+"16%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544051#g=9'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def zapdos_8pt5():
    print("zapdos 8.5's")
    ebay_file = "ebay_zapdos_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_zapdos_8pt5.json"  # json file name that will contain psa data
    price_file = 'prices_zapdos_8pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="zapdos"+"16%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544051#g=8.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def zapdos_8():
    print("zapdos 8's")
    ebay_file = "ebay_zapdos_8.json"  # json file name that will contain eBay data
    psa_file = "psa_zapdos_8.json"  # json file name that will contain psa data
    price_file = 'prices_zapdos_8.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="zapdos"+"16%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544051#g=8'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def zapdos_7pt5():
    print("zapdos 7.5's")
    ebay_file = "ebay_zapdos_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_zapdos_7pt5.json"  # json file name that will contain psa data
    price_file = 'prices_zapdos_7pt5.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="zapdos"+"16%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544051#g=7.5'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


def zapdos_7():
    print("zapdos 7's")
    ebay_file = "ebay_zapdos_7.json"  # json file name that will contain eBay data
    psa_file = "psa_zapdos_7.json"  # json file name that will contain psa data
    price_file = 'prices_zapdos_7.json'
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="zapdos"+"16%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+1st+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/544051#g=7'  # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install())  # open up a chrome application for selenium to use
    driver.get(url)  # give the target url to the driver

    card_data_list = []  # dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult")  # scrape the search results of an ebay search
    card_data_list.append(dict(zip(headers,
                                   ebay_table_headers)))  # input the headers we want listed as the first row (header row) on the website

    for card in cards:  # Scrape search results for the following data from ebay
        card_data = []  # list to append scraped data to

        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = \
        [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # write the auction link and image link into an html line of code to use on the website in order to populate the first column with an image
        html_image = (
                    '<a href=' + auction_link + '><img src=' + image + ' alt="HTML tutorial" style="width:148px;height:225px;"></a>')

        # extend data to the card_data list
        card_data.extend([html_image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)
    price_results = get_prices(psa_file) # get_prices() takes the prices from the psa files and manipulates them.
    # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  # get the avg price and create a fair, good, and great price.


blastoise_10()
blastoise_9pt5()
blastoise_9()
blastoise_8pt5()
blastoise_8()
blastoise_7pt5()
blastoise_7()

alakazam_10()
alakazam_9pt5()
alakazam_9()
alakazam_8pt5()
alakazam_8()
alakazam_7pt5()
alakazam_7()

chansey_10()
chansey_9pt5()
chansey_9()
chansey_8pt5()
chansey_8()
chansey_7pt5()
chansey_7()

charizard_10()
charizard_9pt5()
charizard_9()
charizard_8pt5()
charizard_8()
charizard_7pt5()
charizard_7()

clefairy_10()
clefairy_9pt5()
clefairy_9()
clefairy_8pt5()
clefairy_8()
clefairy_7pt5()
clefairy_7()

gyarados_10()
gyarados_9pt5()
gyarados_9()
gyarados_8pt5()
gyarados_8()
gyarados_7pt5()
gyarados_7()

hitmonchan_10()
hitmonchan_9pt5()
hitmonchan_9()
hitmonchan_8pt5()
hitmonchan_8()
hitmonchan_7pt5()
hitmonchan_7()

magneton_10()
magneton_9pt5()
magneton_9()
magneton_8pt5()
magneton_8()
magneton_7pt5()
magneton_7()

mewtwo_10()
mewtwo_9pt5()
mewtwo_9()
mewtwo_8pt5()
mewtwo_8()
mewtwo_7pt5()
mewtwo_7()

nidoking_10()
nidoking_9pt5()
nidoking_9()
nidoking_8pt5()
nidoking_8()
nidoking_7pt5()
nidoking_7()

ninetales_10()
ninetales_9pt5()
ninetales_9()
ninetales_8pt5()
ninetales_8()
ninetales_7pt5()
ninetales_7()

poliwrath_10()
poliwrath_9pt5()
poliwrath_9()
poliwrath_8pt5()
poliwrath_8()
poliwrath_7pt5()
poliwrath_7()

raichu_10()
raichu_9pt5()
raichu_9()
raichu_8pt5()
raichu_8()
raichu_7pt5()
raichu_7()

venusaur_10()
venusaur_9pt5()
venusaur_9()
venusaur_8pt5()
venusaur_8()
venusaur_7pt5()
venusaur_7()

zapdos_10()
zapdos_9pt5()
zapdos_9()
zapdos_8pt5()
zapdos_8()
zapdos_7pt5()
zapdos_7()