from urllib.request import Request, urlopen
import re

from bs4 import BeautifulSoup

BASE_URL = "http://www.gardnermuseum.org"

def make_soup(url):
	req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
	html = urlopen(req).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('ul', {'class': 'menu__list--left menu__list'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list
    navLinks = [BASE_URL + li.a["href"] for li in nav.findAll("li")]
    return navLinks

# From all navigation links, find current events and exhibitions
def get_link_events(link_url):
    soup = make_soup(link_url)
    events = []
    content = soup.find('ul', {'class':'landing-list-items'}) # find content to search
    for li in content.findAll('li'): #get current events links
    	eventLinks = BASE_URL+ li.a["href"]
    	events.append(eventLinks)
    return events

# From current exhibition links, get relevant dates and information
def get_event_info(event_url):
    soup = make_soup(event_url)

    #GET NAME
    name = ""
    content = soup.find('div', {'id':'block-isgm17-content'}) # find content tag
    h1 = content.find('h1') # find title tag
    # em = h1.find('em')
    name = h1.text # save exhibition name


    #GET DATE AND LOC
    date = ""
    loc = ""
    dateFound = content.find('p', {'class': 'title-card__details'}) # look for date
    date = dateFound.getText().strip()

    # GET DESCRIPTION
    text = ""
    div = soup.find('div', {'class': 'richtext'}) # find div for paragraphs
    for p in div.findAll('p'):
        text += p.getText().strip() # add paragraph texts to empty string


    # GET IMAGES URL
    image = ""
    image_path = content.find('picture', {'class': 'picture__picture'}).find("source").get('data-srcset')
    image = image_path
    if not image_path.startswith('http'):
        image = BASE_URL + image_path
    
    return name, date, loc, text, image

###############################
#### Get information from Isabella Gardner Museum website
#### Currently, information gotten includes for each current exhibit, its title, date, location, and text

def scrape():
    currentExhibitions = [] #list for event links
    allEvents = []

    links = get_nav_links(BASE_URL) #get all navigation links from main page
    for link in links:
        if re.match('(.*)calendar', link, re.I): #find all links with exhibitions
            currentExhibitions = get_link_events(link + "?t=16") #all current event links

    for exh in currentExhibitions: #iterate through to get to each exhibition link
    	#For each distinctive link: return dictionary with url, dates, description, image, and name labels
    	info = {}
    	name,date, loc,text,image = get_event_info(exh) # get info
    	info['url'] = exh; # add value for 'url' key
    	info['dates'] = date
    	info['description'] = text
    	info['image'] = image
    	info['name'] = name
    	info['location'] = loc
    	allEvents.append(info)   		
    return allEvents
