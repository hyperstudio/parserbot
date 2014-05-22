from urllib2 import urlopen
import re 

from bs4 import BeautifulSoup

BASE_URL = "http://www.gardnermuseum.org"

def make_soup(url): 
	html = urlopen(url).read()
	return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    nav = soup.find('ul', {'id': 'nav'}) #find all links from navigation
    #for every "li" found in nav, add to the link to a growing list 
    navLinks = [BASE_URL + li.a["href"] for li in nav.findAll("li")]
    return navLinks

# From all navigation links, find current events and exhibitions
def get_link_events(link_url): 
	soup = make_soup(link_url)
	events = []
	content = soup.find('div', {'id':'content'}) # find content to search  
	for s in content.findAll('span'): # find tags for current works 
		if re.match('(.*)current',s.text,re.I): #find all current exhibitions, disregard past exhibitions or events
			parent = s.findParents('div')[0] # get most recent 'div' parent

			for currentEvents in parent.findAll('ul', {'class': 'subnav_ul divided'}): #get current events links
				eventLinks = [BASE_URL+ li.a["href"] for li in currentEvents.findAll("li")] 
				events = events + eventLinks 
	return events  	

# From current exhibition links, get relevant dates and information
def get_event_info(event_url): 
	soup = make_soup(event_url) 

	#GET NAME
	name = "" 
	content = soup.find('div', {'id':'content'}) # find content tag 
	h1 = content.find('h1') # find title tag 
	# em = h1.find('em')
	name = h1.text # save exhibition name 

	
	#GET DATE AND LOC
	date = ""
	loc = ""
	dateFound = content.find('p', {'class': 'image_details'}) # look for date
	if not dateFound:  
		date = content.find('h4').getText().strip() # other formatting for date possible
	else: 
		date = dateFound.getText().strip()  

	# GET DESCRIPTION
	text = ""
	div = soup.find('div', {'class': 'tab'}) # find div for paragraphs 
	for p in div.findAll('p'): 
		text += p.getText().strip() # add paragraph texts to empty string 

	
	# GET IMAGES URL
	image = ""
	image_path = content.find('div', {'class': 'lightbox_img_link'}).find('img')['src']
	image = (BASE_URL + image_path).strip() 
	
	return name, date, loc, text, image


###############################
#### Get information from Isabella Gardner Museum website 
#### Currently, information gotten includes for each current exhibit, its title, date, location, and text 

def scrape(): 
	currentExhibitions = [] #list for event links
	allEvents = []

	links = get_nav_links(BASE_URL) #get all navigation links from main page
	for link in links: 
		if re.match('(.*)exhibition', link, re.I): #find all links with exhibitions 
			currentExhibitions.append(get_link_events(link)) #all current event links 

	currentExhibitions = currentExhibitions[1:] # get rid of first in list, which is None

	for exhList in currentExhibitions: #iterate through to get to each exhibition link
		for exh in exhList: 
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
