from urllib2 import urlopen
import re 

from bs4 import BeautifulSoup

BASE_URL = "http://www.pem.org"

def make_soup(url): 
	html = urlopen(url).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('ul', {'class': 'mainNav'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list 
    navLinks = [BASE_URL + li.a["href"] for li in nav.findAll("li")]
    return navLinks

# From all navigation links, find all links for events and exhibitions
def get_link_events(link_url): 
	soup = make_soup(link_url)
	div = soup.find('div', {'class':'subNav'}) # find div to search  
	eventLinks = [BASE_URL + li.a["href"] for li in div.findAll("li")] # find all urls for events and exhibitions
	return eventLinks

# From current exhibitions page, find links for current exhibitions
def get_exhibitions(current_url): 
	soup = make_soup(current_url)
	content = soup.find('div', {'class': 'content'}) 
	exhLinks = [BASE_URL + dt.a["href"] for dt in content.findAll("dt")] #build array of exhibition links
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
	for p in feature.findAll('p', {'style':'text-align: justify;'}): 
		text += p.getText() 

	
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

	links = get_nav_links(BASE_URL) #get all navigation links from main page
	for link in links: 
		if re.match('(.*)exhibition', link, re.I): #find all links with exhibitions 
			exhibitions = get_link_events(link) #all exhibition links 

	for exh in exhibitions: 
		if re.match('(.*)current', exh, re.I): #find the link for current events (this can be changed for other desired links)
			currentExhUrl = exh # find current exhibitions link 

	currentExhs = get_exhibitions(currentExhUrl) # array of all current exhibition links 
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

