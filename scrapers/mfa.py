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

	all_link_navs = soup.findAll('div', {'class': 'contextual-links-region'})

	all_links = []
	for link_nav in all_link_navs:
		urls = [tag['href'] for tag in link_nav.findAll('a')]
		for url in urls:
			if not url.startswith('http'):
				url = BASE_URL + url
			if  '/exhibition' in url or '/program' in url:
				all_links.append(url)
	return list(set(all_links))

# From exhibitions page, find all links for events and exhibitions
def get_link_events(link_url):
	soup = make_soup(link_url)
	content_div = soup.find('div', {'class': 'view-content'})
	if content_div is None:
		return []
	eventLinks = list(set([BASE_URL + row['href'] for row in content_div.findAll('a')]))
	return eventLinks


# From exhibition links, get relevant title, dates, and information 
def get_event_info(event_url): 
	soup = make_soup(event_url)

	banner = soup.find('div', {'id': 'banner'})

	# GET NAME
	name = ""
	name = banner.find('h2').getText()
	name = ': '.join([line.strip() for line in name.split('\n')]) # format name nicely

	# GET DATES AND LOC
	date = ""
	dateBox = banner.find('span', {'class': 'date-display-range'})
	if dateBox is not None:
		date = dateBox.getText().strip()
	loc = ""
	loc = dateBox.findNext('br').getText()
	loc = loc.strip()
	
	# GET EVENT DESCRIPTION 
	text = ""
	text = soup.find('div', {'class': 'body'}).getText() # To get text
	
	# GET IMAGE 
	imageURL = ""
	imageURL = banner.findNext('section').find('img')['src']
	if imageURL.startswith('//'):
		imageURL = 'http:' + imageURL
	elif imageURL.startswith('/'):
		imageURL = BASE_URL + imageURL

	return name, date, loc, text, imageURL  


###############################
#### Get information from Peabody Essex Museum website  
#### More information can be added to the 'get_event_info' function to get Related Events, images, and more  
#### Currently, the information for each current exhibit includes its name, date, location, and text 

def scrape(): 
	allEvents = [] #Array for all dictionaries created 

	nav_links = get_nav_links(BASE_URL) #get all navigation links from main page
	nav_links = filter(lambda link: 
		link.endswith('exhibitions') or 'exhibitions/upcoming' in link,
		nav_links)
	exhibitions = [item for sublist in
		[get_link_events(nav_link) for nav_link in nav_links]
		for item in sublist]

	for exh in list(set(exhibitions)):
		try:
			#For each distinctive url: return dictionary with url, dates, description, image, and name labels
			info = {}
			name, date, loc, text, image = get_event_info(exh) # get info 
			info['url'] = exh; # add value for 'url' key 
			info['dates'] = date
			info['location'] = loc 
			info['description'] = text
			info['image'] = image
			info['name'] = name 
			allEvents.append(info)
		except Exception as err:
			print 'Failed on url %s with message %s' % (exh, err.message)
	return allEvents
