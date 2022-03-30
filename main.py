# scraping
from os import system

# system("clear")

import requests
from bs4 import BeautifulSoup


def charizard_9():
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=charizard+base+4%2F102+graded+9&_sacat=183454&LH_TitleDesc=0&_udlo=5000&rt=nc&Language=English&_odkw=charizard+base+4%2F102+graded+10&_osacat=183454&_dcat=183454&Grade=10"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    for i in range(num):  # for the number of "exact" search results, find all titles.
        print(
            soup.find_all("h3", class_="s-item__title")[i + 1].text
        )  # +1 to the incrementer because the first result is always "shop on ebay"


def charizard_10():
    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=charizard%20base%204%2F102%20graded%2010&_sacat=183454&LH_TitleDesc=0&Language=English&Grade=10&_dcat=183454&rt=nc&_udlo=5000"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    num = numOfResults(url)  # find the number of results for the search
    for i in range(num):  # for the number of "exact" search results, find all titles.
        print(
            soup.find_all("h3", class_="s-item__title")[i + 1].text
        )  # +1 to the incrementer because the first result is always "shop on ebay"
        # print(i.get_text())

    # for i in soup.find_all("h3", class_="s-item__title"):
    # print(i.get_text())


# This function finds the number of "exact" search results on the eBay page. eBay shows a number of additional search results that are similar to what you searched for underneath the
# actual search results. We use the resulting number of this function and plug it into the scraper to only gather the first X results.
def numOfResults(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    x = soup.find_all("h1", class_="srp-controls__count-heading")[
        0
    ].text  # find the number of search results line on the web page and store it in 'x' variable
    numOfResults = int(
        x.split()[0]
    )  # read the first word(actually an integer) from the number of search results string into the 'numOfResults' variable, and parse into an int
    return numOfResults


charizard_9()
