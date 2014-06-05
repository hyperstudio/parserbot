from urllib2 import urlopen
import re 

from bs4 import BeautifulSoup

BASE_URL = "http://www.decordova.org"

def make_soup(url): 
	html = urlopen(url).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('ul', {'id': 'nice-menu-1'}) #find all links from navigation
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

	main = soup.find('div', {'id': 'content-area'}) # get link for main exhibit 
	eventLinks.append(BASE_URL + main.find('a')["href"])  

	div = soup.find('div', {'id':'sidebar-left'}) # for exhibition list  
	for listing in div.findAll('p'): # get links for most exhibits
		try:
			eventLinks.append(listing.a["href"]) # find all urls for events and exhibitions
		except TypeError:
			# Sometimes fails due to extra blank p tag
			pass

	return eventLinks


# From exhibition links, get relevant title, dates, and information 
def get_event_info(event_url): 
	soup = make_soup(event_url)
	content = soup.find('div', {'id': 'content-area'})  #for info 
	
	# GET NAME
	name = ""
	name = soup.find('h1').getText().strip() # get exhibition title 

	# GET DATES AND LOC
	date = ""
	if content.find('span', {'class': 'date-display-exhibit-time'}):  
		span = content.find('span', {'class': 'date-display-exhibit-time'})
		date = span.getText().strip() 

	loc = ""
	
	# GET EVENT DESCRIPTION 
	text = "" # String to store all text for the exhibition 
	if content.find('div', {'class': 'tab-content'}): 
		for tab in content.findAll('div', {'class': 'tab-content'}):  # To get text 
			for p in tab.findAll('p'): 
				text += p.getText().strip() 

	if content.find('div', {'class': 'field-body'}): 
		body = content.find('div', {'class': 'field-body'})
		for p in body.findAll('p'): 
				text += p.getText().strip()  
	
	# GET IMAGE 
	imageURL = ""
	img = content.find('div', {'class': 'field-exhibit-feature-image'}) #Find image link 	
	imageURL = img.find('img')['src'].strip()  # add all images associated with event/exhibition

	return name, date, loc, text, imageURL  


###############################
#### Get information from Peabody Essex Museum website  
#### More information can be added to the 'get_event_info' function to get Related Events, images, and more  
#### Currently, the information for each current exhibit includes its name, date, location, and text 

def scrape(): 
	allEvents = [] #Array for all dictionaries created 

	links = get_nav_links(BASE_URL) #get all navigation links from main page
	for link in links: 
		if re.match('(.*)current-exhibitions', link, re.I): #find link for current exhibitions 
	 		exhibitions = get_link_events(link) #all exhibition links 

	 
	for exh in exhibitions: 
		if not re.match('.*trees', exh, re.I): # Hacky, but get rid of permanent tree sculpture list
			# For each distinctive exh: return dictionary with url, dates, description, image, and name labels
			info = {} 	
			name,date, loc, text,image = get_event_info(exh) # get info 
			info['url'] = exh; # add value for 'url' key 
			info['dates'] = date
			info['location'] = loc 
			info['description'] = text
			info['image'] = image
			info['name'] = name 
			allEvents.append(info)  

	return allEvents
