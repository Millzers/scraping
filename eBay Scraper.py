# scraping
# Developed by Logan Miller
# Last updated 3/1/2022
# Must pip install bs4 and html5lib to run code
from time import sleep

import requests
import csv
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#Problems
#1. How to get "pokemon" to show up without foreign characters in csv.
#2.

headers = ['Auction URL', 'Auction Title', 'Current Bid Price', 'Number of Bids', 'Time Left on Auction', 'Link to Image of Auction']


# This function finds the number of "exact" search results on the eBay page. eBay shows a number of additional search
# results that are similar to what you searched for underneath the actual search results. We use the resulting number
# of this function and plug it into the scraper to only gather the first X results.
def numOfResults(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    x = soup.find_all("h1", class_="rsHdr")[ #srp-controls__count-heading // tag for regular search page
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
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)

    table = driver.find_elements(by=By.CSS_SELECTOR, value="#itemResults")[0]
    headers = [header.text for header in table.find_elements(by=By.TAG_NAME, value='th')if header.text != '']
    rows = table.find_elements(by=By.TAG_NAME, value='tbody')[0].find_elements(by=By.TAG_NAME, value='tr')


    results = []

    for row in rows:
        values = [element.text for element in row.find_elements(by=By.TAG_NAME, value='td')if element.text != '']
        print(values)
        results.append(dict(zip(headers, values)))
    print("results = ", results)
    return results

############################################### SCRAPING ALAKAZAM ######################################################

def alakazam_10():
    print("Alakazam 10's")
    ebay_file = "ebay_alakazam_10.json" # json file name that will contain eBay data
    psa_file = "psa_alakazam_10.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"10"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+9%2C+8%2C+7%2C+9.5%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file


def alakazam_9pt5():
    print("Alakazam 9.5's")
    ebay_file = "ebay_alakazam_9pt5.json" # json file name that will contain eBay data
    # psa_file = "psa_alakazam_9pt5.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"9.5"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+10%2C+8%2C+7%2C+9%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    # psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    # psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    # convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

def alakazam_9():
    print("Alakazam 9's")
    ebay_file = "ebay_alakazam_9.json" # json file name that will contain eBay data
    psa_file = "psa_alakazam_9.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"9"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+10%2C+8%2C+7%2C+9.5%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

def alakazam_8pt5():
    print("Alakazam 8.5's")
    ebay_file = "ebay_alakazam_8pt5.json" # json file name that will contain eBay data
    psa_file = "psa_alakazam_8pt5.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"+"10"&_in_kw=1&_ex_kw=1st%2C+shadowless%2C+9%2C+8%2C+7%2C+9.5%2C+8.5%2C+7.5&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

def alakazam_8():
    print("Alakazam 8's")
    ebay_file = "ebay_alakazam_8.json" # json file name that will contain eBay data
    psa_file = "psa_alakazam_8.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"8"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+8.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file



def alakazam_7pt5():
    print("Alakazam 7.5's")
    ebay_file = "ebay_alakazam_7pt5.json" # json file name that will contain eBay data
    psa_file = "psa_alakazam_7pt5.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"7.5"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+8.5+8+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

def alakazam_7():
    print("Alakazam 7's")
    ebay_file = "ebay_alakazam_7.json" # json file name that will contain eBay data
    psa_file = "psa_alakazam_7.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"7"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+8.5+8+7.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

############################################### SCRAPING CHARIZARD #####################################################

def charizard_10():
    print("Charizard 10's")
    ebay_file = "ebay_charizard_10.json" # json file name that will contain eBay data
    psa_file = "psa_charizard_10.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

def charizard_9pt5():
    print("Charizard 9.5's")
    ebay_file = "ebay_charizard_9pt5.json" # json file name that will contain eBay data
    psa_file = "psa_charizard_9pt5.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"9.5"&_in_kw=1&_ex_kw=celebrations+9+10+8.5+8+7.5+7+lot+anniversary+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file


def charizard_9():
    print("Charizard 9's")
    ebay_file = "ebay_charizard_9.json" # json file name that will contain eBay data
    psa_file = "psa_charizard_9.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"9"&_in_kw=1&_ex_kw=celebrations+9.5+10+8.5+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

def charizard_8pt5():
    print("Charizard 8.5's")
    ebay_file = "ebay_charizard_8pt5.json" # json file name that will contain eBay data
    psa_file = "psa_charizard_8pt5.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"8.5"&_in_kw=1&_ex_kw=celebrations+9.5+10+9+8+7.5+7+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

def charizard_8():
    print("Charizard 8's")
    ebay_file = "ebay_charizard_8.json" # json file name that will contain eBay data
    psa_file = "psa_charizard_8.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"8"&_in_kw=1&_ex_kw=celebrations+9.5+10+9+8.5+7.5+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

def charizard_7pt5():
    print("Charizard 7.5's")
    ebay_file = "ebay_charizard_7pt5.json" # json file name that will contain eBay data
    psa_file = "psa_charizard_7pt5.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"7.5"&_in_kw=1&_ex_kw=celebrations+9.5+10+9+8.5+8+7+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file

def charizard_7():
    print("Charizard 7's")
    ebay_file = "ebay_charizard_7.json" # json file name that will contain eBay data
    psa_file = "psa_charizard_7.json" # json file name that will contain psa data
    # url for eBay auction
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+9.5+10+9+8.5+8+7.5+if+lot+anniversary+blastoise+venusaur+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    psa_url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10' # url for PSA website

    driver = webdriver.Chrome(ChromeDriverManager().install()) #open up a chrome application for selenium to use
    driver.get(url) #give the target url to the driver

    card_data = [] #list to append scraped data to
    card_data_list = [] #dictionary that will be zipped with card_data[] list & headers[] list

    cards = driver.find_elements(by=By.CLASS_NAME, value="sresult") #scrape the search results of an ebay search

    for card in cards: #Scrape search results for the following data from ebay
        title = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvtitle")][0]
        price = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvprice")][0]
        number_of_bids = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="lvformat")][0]
        time_left = [element.text for element in card.find_elements(by=By.CLASS_NAME, value="tme")][0]
        image = [element.get_attribute("src") for element in card.find_elements(by=By.TAG_NAME, value="img")][0]
        auction_link = [element.get_attribute("href") for element in card.find_elements(By.CSS_SELECTOR, "h3.lvtitle > a[href]")][0]

        # extend data to the card_data list
        card_data.extend([image])
        card_data.extend([title])
        card_data.extend([price])
        card_data.extend([number_of_bids])
        card_data.extend([time_left])
        card_data.extend([auction_link])


        card_data_list.append(dict(zip(headers, card_data))) #join the headers[] list with the card_data we just scraped

    # call getMarketPrice function which scrapes the PSA website. Return results to psa_results
    psa_results = getMarketPrice(psa_url)

    convert_to_json(card_data_list, ebay_file) #convert the list of dictionaries from eBay to a json file
    convert_to_json(psa_results, psa_file) #convert the list of dictionaries from psa to a json file


alakazam_10()
alakazam_9pt5()
alakazam_9()
alakazam_8pt5()
alakazam_8()
alakazam_7pt5()
alakazam_7()
#charizard_10()
#charizard_9pt5()
#charizard_9()
#charizard_8pt5()
#charizard_8()

