from urllib.request import Request, urlopen
import re
import datetime

from bs4 import BeautifulSoup

BASE_URL = "http://www.pem.org"

def make_soup(url):
	req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
	html = urlopen(req).read()
	return BeautifulSoup(html)
	
#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('ul', {'class': 'header__nav-list'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list
    navLinks = [BASE_URL + li.a["href"] for li in nav.findAll("li")[:-2]]
    return navLinks

# From current exhibitions page, find links for current exhibitions
def get_exhibitions(current_url):
    soup = make_soup(current_url)
    exhLinks = []
    content = soup.find('div', {'class': 'mod-whats-on__results fadable js-results'})
    return exhLinks

# From current exhibition links, get relevant title, dates, and information
def get_event_info(event_url):
    soup = make_soup(event_url)
    feature = soup.find('div', {'class': 'feature_detail'}) #General wrapper for all event details
    info = feature.find('div', {'class': 'info'})

    # GET NAME
    name = ""
    name = feature.find('h2').getText().strip() # get exhibition title

    # GET DATES
    date = "" #String to store dates and location
    dates = feature.find('p', {'class':'dates'}) # get the first 'p' tag, which is date
    date += dates.getText().strip()

    #GET LOCATION
    loc = ""
    locs = dates.findNextSibling() #second p tag is loc
    loc += locs.getText().strip()


    # GET EVENT DESCRIPTION
    text = "" # String to store all text for the exhibition
    grafs = feature.findAll('p', {'style':'text-align: justify;'})
    if not grafs:
        grafs = feature.findAll('p')
    for graf in grafs:
        text += graf.getText()


    # GET IMAGE
    imageURL = ""
    featureImg = soup.find('div', {'class': 'feature_image'}) # Find image tag
    img = feature.find('img') #Find all image tags
    imageURL = BASE_URL + img['src']  # add all images associated with event/exhibition


    return name, date, loc, text, imageURL


###############################
#### Get information from Peabody Essex Museum website
#### More information can be added to the 'get_event_info' function to get Related Events, images, and more
#### Currently, the information for each current exhibit includes its name, date, location, and text

def scrape():
    allEvents = [] #Array for all dictionaries created
    currentExhs = []

    links = get_nav_links(BASE_URL) #get all navigation links from main page
    for link in links:
        if re.match('(.*)___whats-on', link, re.I): #find all links with exhibitions
            currentExhs = get_exhibitions(link) # array of all current exhibition links
            
    for exh in currentExhs:
        # For each distinctive exh: return dictionary with url, dates, description, image, and name labels
            #For each distinctive url: return dictionary with url, dates, description, image, and name labels
            info = {}
            name,date, loc, text,image = get_event_info(exh) # get info
            info['url'] = exh; # add value for 'url' key
            info['dates'] = date
            info['description'] = text
            info['image'] = image
            info['name'] = name
            info['location'] = loc
            allEvents.append(info)


    return allEvents

print(scrape())