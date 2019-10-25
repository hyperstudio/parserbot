from urllib.request import Request, urlopen
import re

from bs4 import BeautifulSoup

BASE_URL = "http://www.icaboston.org/"

def make_soup(url):
	req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
	html = urlopen(req).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('div', {'class': 'menu-block-wrapper menu-block-2 menu-name-main-menu parent-mlid-0 menu-level-1'}).find('ul') #find all links from navigation
    navLinks = []

    #for every "li" found in nav, add to the link to a growing list
    for li in nav.findAll('li'):
    	link = BASE_URL + li.a["href"] # exhibition link to be added
    	if link not in navLinks:
    		navLinks.append(link)  # add only if not already in list
    return navLinks

# From exhibitions page, find all links for events and exhibitions
def get_link_events(link_url):
    soup = make_soup(link_url)

    eventLinks = []
    main = soup.find('div', {'class': 'item-list'}).find('ul') # get links for main exhibits
    for li in main.findAll('li'):
        url = li.a['href']
        eventLinks.append(BASE_URL + url)
    return eventLinks


# From exhibition links, get relevant title, dates, and information
def get_event_info(event_url):
    soup = make_soup(event_url)
    content = soup.find('div', {'class': 'content'})  #for info

    # GET NAME
    name = ""
    name = soup.find('h1').getText().strip() # get exhibition title

    # GET DATES AND LOC
    date = ""
    div = soup.find('div', {'class': 'field field-name-exhibition-date field-type-ds field-label-hidden items-few items-1 jump-target'})
    date = div.getText().strip()

    loc = ""

    # GET EVENT DESCRIPTION
    text = "" # String to store all text for the exhibition
    cont = soup.find('div', {'class': 'ds-1col node node-exhibition view-mode-full clearfix'})
    for p in cont.findAll('p'):
    	text += p.getText().strip()
        
    # GET IMAGE
    imageURL = ""
    img = soup.find('div', {'class': 'field field-name-scald-thumbnail field-type-image field-label-hidden items-few items-1 jump-target'}) #Find image link
    imageURL = img.find('img')['src'].strip()  # add all images associated with event/exhibition

    return name, date, loc, text, imageURL


###############################
#### Get information from DeCordova website
#### More information can be added to the 'get_event_info' function to get Related Events, images, and more
#### Currently, the information for each current exhibit includes its name, date, location, and text

def scrape():
    allEvents = [] #Array for all dictionaries created
    exhibitions = []

    links = get_nav_links(BASE_URL) #get all navigation links from main page
    for link in links:
    	if re.match('(.*)exhibitions', link, re.I): #find link for current exhibitions
    		exhibitions = get_link_events(link) #all exhibition links

    for exh in exhibitions:
        try:
        	info = {}
        	name,date, loc, text,image = get_event_info(exh) # get info
        	info['url'] = exh; # add value for 'url' key
        	info['dates'] = date
        	info['location'] = loc
        	info['description'] = text
        	info['image'] = image
        	info['name'] = name
        except AttributeError:
        	continue
        else:
        	allEvents.append(info)
    return allEvents