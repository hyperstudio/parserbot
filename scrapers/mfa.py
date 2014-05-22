from urllib2 import urlopen
import re 

from bs4 import BeautifulSoup

BASE_URL = "http://www.mfa.org"

def make_soup(url): 
	html = urlopen(url).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('div', {'id': 'navDropContent'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list 
    navLinks = [BASE_URL + li.a["href"] for li in nav.findAll("li")]
    return navLinks

# From exhibitions page, find all links for events and exhibitions
def get_link_events(link_url): 
	soup = make_soup(link_url)
	eventLinks = [] 

	div = soup.find('div', {'id':'mainColumn'}) # find div to search  

	showcase = div.find('div', {'class': 'showcase'}) # get link for showcase exhibit 
	eventLinks.append(BASE_URL + showcase.a["href"])  

	for listing in div.findAll('div', {'class': 'listing-text'}): # get links for most exhibits 
		eventLinks.append(BASE_URL + listing.a["href"]) # find all urls for events and exhibitions

	return eventLinks


# From exhibition links, get relevant title, dates, and information 
def get_event_info(event_url): 
	soup = make_soup(event_url) 
	main = soup.find('div', {'id': 'mainColumn'}) #General wrapper for all event details
	showcase = main.find('div', {'class': 'showcase'}) # For title, dates, location 
	
	# GET NAME
	name = ""
	name = showcase.find('h1').getText() # get exhibition title 
	name = re.sub('[\t\r\n]*', '', name) # remove extra white space

	# GET DATES AND LOC
	date = ""
	loc = ""
	box = showcase.find('div', {'class': 'red-box-links'})
	date = box.find('strong').getText().strip() 
	match = box.find('p').getText() 
	loc = re.sub(date, '', match) # extract location from text gotten from date 
	loc = loc.strip()  

	
	# GET EVENT DESCRIPTION 
	text = ""
	left = soup.find('div', {'id': 'mainLeftColumn'}) # To get text 
	text = "" # String to store all text for the exhibition 
	for p in left.findAll('p'): 
		text += p.getText().strip() 

	
	# GET IMAGE 
	imageURL = ""
	img = showcase.find('img') #Find image link 	
	imageURL = (BASE_URL + img['src']).strip()  # add all images associated with event/exhibition

	return name, date, loc, text, imageURL  


###############################
#### Get information from Peabody Essex Museum website  
#### More information can be added to the 'get_event_info' function to get Related Events, images, and more  
#### Currently, the information for each current exhibit includes its name, date, location, and text 

def scrape(): 
	allEvents = [] #Array for all dictionaries created 

	links = get_nav_links(BASE_URL) #get all navigation links from main page
	for link in links: 
		if re.match('(.*)exhibitions$', link, re.I): #find link for current exhibitions 
	 		exhibitions = get_link_events(link) #all exhibition links 


	for exh in exhibitions: 
		# For each distinctive exh: return dictionary with url, dates, description, image, and name labels
			#For each distinctive url: return dictionary with url, dates, description, image, and name labels
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
