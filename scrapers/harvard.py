
from urllib2 import urlopen
import re 
from bs4 import BeautifulSoup

BASE_URL = "http://www.harvardartmuseums.org"


def make_soup(url): 
	html = urlopen(url).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('ul', {'id': 'main-menu'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list 
    navLinks = [BASE_URL + li.a["href"] for li in nav.findAll("li")]
    return navLinks

# From all navigation links, find all links for events and exhibitions
def get_link_events(link_url): 
	soup = make_soup(link_url)
	eventLinks = []
	content = soup.find('section', {'id':'section-content'}) # Find where event links are stored
	for field in content.findAll('div', {'class':'field-item even'}):  # find div to search  
		if field.find("a"): 
			eventURL = BASE_URL + field.a["href"] 
			if re.match('^/', field.a["href"]) and (eventURL not in eventLinks): # Sort out the non-event links 
				eventLinks.append(eventURL)# add only the event links 
	
	return eventLinks

# From current exhibition links, get relevant title, dates, and information 
def get_event_info(event_url): 
	soup = make_soup(event_url) 
	section = soup.find('section', {'id': 'section-content'}) #General wrapper for all event details
	time = "" 
	loc = "" 
	text = "" 
	date = "" 
	title = "" 

	for content in section.findAll('div', {'class' :'content clearfix'}): 
		for div in content.findAll('div'): 
			if div.has_attr('class'): 
				listTags = div['class'] #Filter for correct tag in all tags 

				# GET ALL NAME, DATE, TIME, TEXT, IMAGE INFO 
				for tag in listTags:  
					if re.match('(.*)field-name-field(.*)-title',tag,re.I): #Match for title
						title = div.find('div', {'class': 'field-item even'}).text.strip() 
					if re.match('(.*)field-name-field(.*)date',tag,re.I): #Match for date
						date = div.find('div', {'class': 'field-item even'}).text.strip()  
					if re.match('(.*)field-name-field(.*)time',tag,re.I): #Match tag for time 
						time = div.find('div', {'class': 'field-item even'}).text.strip()  
					if re.match('(.*)field-name-field(.*)location',tag,re.I): #Match tag for location
						loc = div.find('div', {'class': 'field-item even'}).text.strip()  
					if re.match('(.*)field-(.*)summary',tag,re.I): #Match tag for text description
						text = div.find('div', {'class': 'field-item even'}).text.strip()  
					if re.match('(.*)field-name-field(.*)image$', tag, re.I):  #Match tag for image files 
						if div.find('div', {'class': 'field-item even'}): 
							img = div.find('div', {'class': 'field-item even'}).find('img')
							image = (img['src']).strip() 
				
	date = "%s %s" % (date, time) # consolidate date, time info 

	return title, date, loc, text, image 
	

###############################
#### Get events information from Harvard Art Museums website 
#### Currently, all information for the event is captured 

def scrape(): 
	allEvents = [] #List for all dictionaries 

	links = get_nav_links(BASE_URL) #get all navigation links from main page

	for link in links: 
		if re.match('(.*)calendar', link, re.I): #find the calendar link 
			events = get_link_events(link) #all exhibition links 

	for event in events: 
	 	#For each distinctive link: return dictionary with url, dates, description, image, and name labels
			info = {} 	
			name,date, loc, text,images = get_event_info(event) # get info 
			info['url'] = event; # add value for 'url' key 
			info['dates'] = date
			info['description'] = text
			info['image'] = images
			info['name'] = name 
			info['location'] = loc 
			allEvents.append(info)  
 

	return allEvents 


	