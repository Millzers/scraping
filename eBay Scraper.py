# scraping
# Developed by Logan Miller
# Last updated 3/1/2022
# Must pip install bs4 and html5lib to run code

import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Problems
# 1. How to get "pokemon" to show up without foreign characters
# 2.

headers = ['Auction URL', 'Auction Title', 'Current Bid Price', 'Number of Bids', 'Time Left on Auction',
           'Link to Image of Auction']
ebay_table_headers = ['Auction Image', 'Auction Title', 'Current Bid Price', 'Number of Bids', 'Time Left on Auction']
psa_table_headers = []


# This function finds the number of "exact" search results on the eBay page. eBay shows a number of additional search
# results that are similar to what you searched for underneath the actual search results. We use the resulting number
# of this function and plug it into the scraper to only gather the first X results.
def numOfResults(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    x = soup.find_all("h1", class_="rsHdr")[  # srp-controls__count-heading // tag for regular search page
        0
    ].text  # find the number of search results line on the web page and store it in 'x' variable
    numOfResults = int(
        x.split()[0]
    )  # read the first word(actually an integer) from the number of search results string into the 'numOfResults'
    # variable, and parse into an int
    return numOfResults


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


def getMarketPrice(url):
    i = 0
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)

    table = driver.find_elements(by=By.CSS_SELECTOR, value="#itemResults")[0]
    headers = [header.text for header in table.find_elements(by=By.TAG_NAME, value='th') if header.text != '']
    rows = table.find_elements(by=By.TAG_NAME, value='tbody')[0].find_elements(by=By.TAG_NAME, value='tr')

    results = []
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
    # open the .json file that contains the PSA data for the card.
    with open(file, 'r') as json_file:
        json_load = json.load(json_file)

    for x in json_load:  # for every dictionary in json_load
        prices += float(x['PRICE'].lstrip("$"))  # get the values with the 'PRICES' key

    most_recent = json_load[0]  # get the most recent sale
    fresh_price = float(most_recent['PRICE'].lstrip("$"))  # get the price for the most recent sale
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

        card_data_list.append(
            dict(zip(headers, card_data)))  # join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)
    price_results = get_prices(psa_file)  ############################################
    print(price_results)

    convert_to_json(card_data_list, ebay_file)  # convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file
    convert_to_json(price_results, price_file)  ############################################


def alakazam_9pt5():
    print("Alakazam 9.5's")
    ebay_file = "ebay_alakazam_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_9pt5.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"9.5"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+10%2C+8%2C+7%2C+9%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def alakazam_9():
    print("Alakazam 9's")
    ebay_file = "ebay_alakazam_9.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_9.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"9"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+10%2C+8%2C+7%2C+9.5%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def alakazam_8pt5():
    print("Alakazam 8.5's")
    ebay_file = "ebay_alakazam_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_8pt5.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"10"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+9%2C+8%2C+7%2C+9.5%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def alakazam_8():
    print("Alakazam 8's")
    ebay_file = "ebay_alakazam_8.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_8.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"8"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+8.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def alakazam_7pt5():
    print("Alakazam 7.5's")
    ebay_file = "ebay_alakazam_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_7pt5.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"7.5"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+8.5+8+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def alakazam_7():
    print("Alakazam 7's")
    ebay_file = "ebay_alakazam_7.json"  # json file name that will contain eBay data
    psa_file = "psa_alakazam_7.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"7"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+8.5+8+7.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


############################################### SCRAPING CHARIZARD #####################################################

def charizard_10():
    print("Charizard 10's")
    ebay_file = "ebay_charizard_10.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_10.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def charizard_9pt5():
    print("Charizard 9.5's")
    ebay_file = "ebay_charizard_9pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_9pt5.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def charizard_9():
    print("Charizard 9's")
    ebay_file = "ebay_charizard_9.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_9.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def charizard_8pt5():
    print("Charizard 8.5's")
    ebay_file = "ebay_charizard_8pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_8pt5.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def charizard_8():
    print("Charizard 8's")
    ebay_file = "ebay_charizard_8.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_8.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def charizard_7pt5():
    print("Charizard 7.5's")
    ebay_file = "ebay_charizard_7pt5.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_7pt5.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


def charizard_7():
    print("Charizard 7's")
    ebay_file = "ebay_charizard_7.json"  # json file name that will contain eBay data
    psa_file = "psa_charizard_7.json"  # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'  # url for PSA website

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
    convert_to_json(psa_results, psa_file)  # convert the list of dictionaries from psa to a json file


alakazam_10()
alakazam_9pt5()
alakazam_9()
alakazam_8pt5()
alakazam_8()
alakazam_7pt5()
alakazam_7()
# charizard_10()
# charizard_9pt5()
# charizard_9()
# charizard_8pt5()
# charizard_8()
