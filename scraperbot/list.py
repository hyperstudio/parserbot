from urllib.request import Request, urlopen
import re

from bs4 import BeautifulSoup

BASE_URL = "http://listart.mit.edu"

def make_soup(url):
	req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
	html = urlopen(req).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    navLinks = []
    nav = soup.find('nav', {'class': 'navigation primary-navigation'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list
    for li in nav.findAll('li'):
        URL = BASE_URL + li.a["href"]
        if URL not in navLinks:
            navLinks.append(URL)
    return navLinks

# From all navigation links, find current events and exhibitions
def get_link_events(link_url):
    soup = make_soup(link_url)
    events = []
    content = soup.find('ul', {'class':'current-exhibitions'}) # find content to search

    for article in content.findAll('article'):
        eventLink = BASE_URL + article.a["href"]
        if eventLink not in events:
            events.append(eventLink)
    return events

# From current exhibition links, get relevant dates and information
def get_exhibition_info(exh_url):
    soup = make_soup(exh_url)
    section = soup.find('div', {'class': 'main-wrapper'})

    #GET NAME
    name = ""
    page = section.find('div', {'class':'page'}) # find content tag
    h1 = page.find('h1') # find title tag
    name = h1.text.strip() # save exhibition name

    #GET DATE AND LOC
    date = ""
    date = page.find('span',{'class':'subject'}).text.strip() # find date text
    loc = ""
    h2 = page.find('h2')
    loc = h2.text.strip()

    # GET DESCRIPTION
    text = ""
    div = soup.find('div', {'class': 'body'}) # find div for paragraphs
    for p in div.findAll('p'):
        text += p.getText().strip() # add paragraph texts to empty string

    # GET IMAGES URL
    image = ""
    img = section.find('li', {'class': 'active'})
    image = (img.find('img')['src']).strip()

    return name, date, loc, text, image


###############################
#### Get information from Isabella Gardner Museum website
#### Currently, information gotten includes for each current exhibit, its title, date, location, and text

def scrape():
    current = [] #list for event links
    allEvents = []

    links = get_nav_links(BASE_URL) #get all navigation links from main page
    for link in links:
        if re.match('(.*)exhibitions$', link, re.I): #find current exhibitions
            current = get_link_events(link) #all current event links

    for exh in current: #iterate through to get to each exhibition link
        #For each distinctive link: return dictionary with url, dates, description, image, and name labels
        info = {}
        name,date,loc,text,image = get_exhibition_info(exh) # get info
        info['url'] = exh; # add value for 'url' key
        info['dates'] = date
        info['location'] = loc
        info['description'] = text
        info['image'] = image
        info['name'] = name
        allEvents.append(info)

    return allEvents