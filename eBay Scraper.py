# scraping
# Developed by Logan Miller
# Last updated 3/1/2022
# Must pip install bs4 and html5lib to run code
from time import sleep

import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import cx_Oracle

# Connect string format: [username]/[password]@//[hostname]:[port]/[DB service name]
#conn = cx_Oracle.connect("[sys]/[charizard]@//localhost:1521/xe") #XEPDB1
#cur = conn.cursor()
#cur.execute("SELECT 'Hello World!' FROM dual")
#res = cur.fetchall()
#print(res)

#Problems
#1. How to get "pokemon" to show up without foreign characters in csv.
#2. How to scrape time remaining
#3.

#header = ['Listing Title', 'Current Bid Price', 'Number of Bids', 'Time Left on Auction', 'Link to Image of Auction']

driver = webdriver.Chrome(ChromeDriverManager().install())



def alakazam_10():
    print("Alakazam 10's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"10"&_in_kw=1&_ex_kw=9.5+celebrations+9+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    with open('alakazam_10.csv', 'w', encoding='UTF8', newline='') as f:
        for i in range(num):  # for the number of "exact" search results, find all titles.
            title = soup.find_all("h3", class_="lvtitle")[i].text.strip()
            print(title)
            price = soup.find_all("li", class_="lvprice prc")[i].text.strip()
            print(price)
            numOfBids = soup.find_all("li", class_="lvformat")[i].text.strip()
            print(numOfBids)
            # timeLeft = soup.find_all("span", class_="tme")[i].text.strip()
            # print(timeLeft)
            image = soup.find_all("img", attrs={"class": "img"})[i]
            print(
                image.attrs['src'].strip()
            )
    getMarketPrice()

def alakazam_9pt5():
    print("Alakazam 9.5's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"9.5"&_in_kw=1&_ex_kw=10+celebrations+9+8+8.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    with open('alakazam_9pt5.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(num):  # for the number of "exact" search results, find all titles.
            title = soup.find_all("h3", class_="lvtitle")[i].text.strip()
            print(title)
            writer.writerow([title])  # (soup.find_all("h3", class_="lvtitle")[i]
            price = soup.find_all("li", class_="lvprice prc")[i].text.strip()
            print(price)
            writer.writerow([price])
            numOfBids = soup.find_all("li", class_="lvformat")[i].text.strip()
            print(numOfBids)
            writer.writerow([numOfBids])
            # timeLeft = soup.find_all("span", class_="tme")[i].text.strip()
            # print(timeLeft)
            image = soup.find_all("img", attrs={"class": "img"})[i]
            print(
                image.attrs['src'].strip()
            )
            writer.writerow([image.attrs['src'].strip()])
            writer.writerow(" ")  # writes a blank row to make csv look clean.

def alakazam_9():
    print("Alakazam 9's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"9"&_in_kw=1&_ex_kw=10+celebrations+8+8.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    with open('alakazam_9.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(num):  # for the number of "exact" search results, find all titles.
            title = soup.find_all("h3", class_="lvtitle")[i].text.strip()
            print(title)
            writer.writerow([title])  # (soup.find_all("h3", class_="lvtitle")[i]
            price = soup.find_all("li", class_="lvprice prc")[i].text.strip()
            print(price)
            writer.writerow([price])
            numOfBids = soup.find_all("li", class_="lvformat")[i].text.strip()
            print(numOfBids)
            writer.writerow([numOfBids])
            # timeLeft = soup.find_all("span", class_="tme")[i].text.strip()
            # print(timeLeft)
            image = soup.find_all("img", attrs={"class": "img"})[i]
            print(
                image.attrs['src'].strip()
            )
            writer.writerow([image.attrs['src'].strip()])
            writer.writerow(" ")  # writes a blank row to make csv look clean.

def alakazam_8pt5():
    print("Alakazam 8.5's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"8.5"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    with open('alakazam_8pt5.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(num):  # for the number of "exact" search results, find all titles.
            title = soup.find_all("h3", class_="lvtitle")[i].text.strip()
            print(title)
            writer.writerow([title])  # (soup.find_all("h3", class_="lvtitle")[i]
            price = soup.find_all("li", class_="lvprice prc")[i].text.strip()
            print(price)
            writer.writerow([price])
            numOfBids = soup.find_all("li", class_="lvformat")[i].text.strip()
            print(numOfBids)
            writer.writerow([numOfBids])
            # timeLeft = soup.find_all("span", class_="tme")[i].text.strip()
            # print(timeLeft)
            image = soup.find_all("img", attrs={"class": "img"})[i]
            print(
                image.attrs['src'].strip()
            )
            writer.writerow([image.attrs['src'].strip()])
            writer.writerow(" ")  # writes a blank row to make csv look clean.

def alakazam_8():
    print("Alakazam 8's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"8"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    with open('alakazam_8.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(num):  # for the number of "exact" search results, find all titles.
            title = soup.find_all("h3", class_="lvtitle")[i].text.strip()
            print(title)
            writer.writerow([title])  # (soup.find_all("h3", class_="lvtitle")[i]
            price = soup.find_all("li", class_="lvprice prc")[i].text.strip()
            print(price)
            writer.writerow([price])
            numOfBids = soup.find_all("li", class_="lvformat")[i].text.strip()
            print(numOfBids)
            writer.writerow([numOfBids])
            # timeLeft = soup.find_all("span", class_="tme")[i].text.strip()
            # print(timeLeft)
            image = soup.find_all("img", attrs={"class": "img"})[i]
            print(
                image.attrs['src'].strip()
            )
            writer.writerow([image.attrs['src'].strip()])
            writer.writerow(" ")  # writes a blank row to make csv look clean.

def alakazam_7pt5():
    print("Alakazam 7.5's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"7.5"&_in_kw=1&_ex_kw=10+celebrations+9+9.5+7+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    with open('alakazam_7pt5.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(num):  # for the number of "exact" search results, find all titles.
            title = soup.find_all("h3", class_="lvtitle")[i].text.strip()
            print(title)
            writer.writerow([title])  # (soup.find_all("h3", class_="lvtitle")[i]
            price = soup.find_all("li", class_="lvprice prc")[i].text.strip()
            print(price)
            writer.writerow([price])
            numOfBids = soup.find_all("li", class_="lvformat")[i].text.strip()
            print(numOfBids)
            writer.writerow([numOfBids])
            # timeLeft = soup.find_all("span", class_="tme")[i].text.strip()
            # print(timeLeft)
            image = soup.find_all("img", attrs={"class": "img"})[i]
            print(
                image.attrs['src'].strip()
            )
            writer.writerow([image.attrs['src'].strip()])
            writer.writerow(" ")  # writes a blank row to make csv look clean.

def alakazam_7():
    print("Alakazam 7's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="alakazam"+"1%2F102"++"7"&_in_kw=1&_ex_kw=10+celebrations+9+9.5++shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    with open('alakazam_7.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(num):  # for the number of "exact" search results, find all titles.
            title = soup.find_all("h3", class_="lvtitle")[i].text.strip()
            print(title)
            writer.writerow([title])  # (soup.find_all("h3", class_="lvtitle")[i]
            price = soup.find_all("li", class_="lvprice prc")[i].text.strip()
            print(price)
            writer.writerow([price])
            numOfBids = soup.find_all("li", class_="lvformat")[i].text.strip()
            print(numOfBids)
            writer.writerow([numOfBids])
            # timeLeft = soup.find_all("span", class_="tme")[i].text.strip()
            # print(timeLeft)
            image = soup.find_all("img", attrs={"class": "img"})[i]
            print(
                image.attrs['src'].strip()
            )
            writer.writerow([image.attrs['src'].strip()])
            writer.writerow(" ")  # writes a blank row to make csv look clean.

def charizard_10():
    print("Charizard 10's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"10"&_in_kw=1&_ex_kw=9.5+celebrations+9+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    with open('charizard_10.csv', 'w', encoding='UTF8', newline='') as f:
        for i in range(num):  # for the number of "exact" search results, find all titles.
            title = soup.find_all("h3", class_="lvtitle")[i].text.strip()
            print(title)
            price = soup.find_all("li", class_="lvprice prc")[i].text.strip()
            print(price)
            numOfBids = soup.find_all("li", class_="lvformat")[i].text.strip()
            print(numOfBids)
            #timeLeft = soup.find_all("span", class_="tme")[i].text.strip()
            #print(timeLeft)
            image = soup.find_all("img", attrs={"class": "img"})[i]
            print(
                image.attrs['src'].strip()
            )

def charizard_9pt5():
    print("Charizard 9.5's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"9.5"&_in_kw=1&_ex_kw=9+celebrations+8.5+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    for i in range(num):  # for the number of "exact" search results, find all titles.
        print(
            soup.find_all("h3", class_="lvtitle")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="lvprice prc")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="lvformat")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="timeleft")[i].text.strip()
        )
        image = soup.find_all("img", attrs={"class": "img"})[i]
        print(
            image.attrs['src'].strip()
        )

def charizard_9():
    print("Charizard 9's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_dcat=183454&Grade=9&_nkw="charizard"+"4%2F102"++"9"&_in_kw=1&_ex_kw=8.5+celebrations+8+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    for i in range(num):  # for the number of "exact" search results, find all titles.
        print(
            soup.find_all("h3", class_="lvtitle")[i].text.strip()
        )  # +1 to the incrementer because the first result is always "shop on ebay"
        print(
            soup.find_all("li", class_="lvprice prc")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="lvformat")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="timeleft")[i].text.strip()
        )
        image = soup.find_all("img", attrs={"class": "img"})[i]
        print(
            image.attrs['src'].strip()
        )

def charizard_8pt5():
    print("Charizard 8.5's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"8.5"&_in_kw=1&_ex_kw=8+celebrations+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    for i in range(num):  # for the number of "exact" search results, find all titles.
        print(
            soup.find_all("h3", class_="lvtitle")[i].text.strip()
        )  # +1 to the incrementer because the first result is always "shop on ebay"
        print(
            soup.find_all("li", class_="lvprice prc")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="lvformat")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="timeleft")[i].text.strip()
        )
        image = soup.find_all("img", attrs={"class": "img"})[i]
        print(
            image.attrs['src'].strip()
        )

def charizard_8():
    print("Charizard 8's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"8"&_in_kw=1&_ex_kw=7.5+celebrations+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    for i in range(num):  # for the number of "exact" search results, find all titles.
        print(
            soup.find_all("h3", class_="lvtitle")[i].text.strip()
        )  # +1 to the incrementer because the first result is always "shop on ebay"
        print(
            soup.find_all("li", class_="lvprice prc")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="lvformat")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="timeleft")[i].text.strip()
        )
        image = soup.find_all("img", attrs={"class": "img"})[i]
        print(
            image.attrs['src'].strip()
        )

def charizard_7pt5():
    print("Charizard 7.5's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"7.5"&_in_kw=1&_ex_kw=+celebrations+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    for i in range(num):  # for the number of "exact" search results, find all titles.
        print(
            soup.find_all("h3", class_="lvtitle")[i].text.strip()
        )  # +1 to the incrementer because the first result is always "shop on ebay"
        print(
            soup.find_all("li", class_="lvprice prc")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="lvformat")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="timeleft")[i].text.strip()
        )
        image = soup.find_all("img", attrs={"class": "img"})[i]
        print(
            image.attrs['src'].strip()
        )

def charizard_7():
    print("Charizard 7's")
    url = 'https://www.ebay.com/sch/CCG-Individual-Cards/183454/i.html?_from=R40&_nkw="charizard"+"4%2F102"++"7"&_in_kw=1&_ex_kw=celebrations+shadowless+gold+reverse+service+reprint+other&_sacat=183454&_udlo=&_udhi=&LH_Auction=1&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=32413&_sargn=-1%26saslc%3D1&_salic=1&_sop=15&_dmd=1&_ipg=60&_fosrp=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    for i in range(num):  # for the number of "exact" search results, find all titles.
        print(
            soup.find_all("h3", class_="lvtitle")[i].text.strip()
        )  # +1 to the incrementer because the first result is always "shop on ebay"
        print(
            soup.find_all("li", class_="lvprice prc")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="lvformat")[i].text.strip()
        )
        print(
            soup.find_all("li", class_="timeleft")[i].text.strip()
        )
        image = soup.find_all("img", attrs={"class": "img"})[i]
        print(
            image.attrs['src'].strip()
        )


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

def getMarketPrice():
    url = 'https://www.psacard.com/auctionprices/tcg-cards/1999-pokemon-game/alakazam-holo/values/702171#g=10'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)
    marketPrice = driver.find_elements_by_xpath('//*[@id="itemResults"]/tbody/tr[1]/td[4]')
    price = []
    for i in range(len(marketPrice)):
        price.append(marketPrice[i].text)
    print(price)



getMarketPrice()
#def getAuctionPrice(url):
#    r = requests.get(url)
#   soup = BeautifulSoup(r.content, "html5lib")
#    x = soup.find_all("li", class_="lvprice prc")[  # srp-controls__count-heading
#        0
#    ].text  # find the number of search results line on the web page and store it in 'x' variable
#    numOfResults = int(
#        x.split()[0]
#    )

#alakazam_10()
#alakazam_9pt5()
#alakazam_9()
#alakazam_8pt5()
#alakazam_8()
#alakazam_7pt5()
#alakazam_7()
#charizard_10()
#charizard_9pt5()
#charizard_9()
#charizard_8pt5()
#charizard_8()

