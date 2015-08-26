from urllib2 import urlopen
import re
from bs4 import BeautifulSoup
from urlparse import urlparse, urljoin

BASE_URL = "http://www.harvardartmuseums.org"

def strip_args(url):
    """ Accepts URL as a string and strips arguments, avoiding flags """
    for i in range(len(url)):
        if url[i] == "?" or url[i] == "#":
            return url[:i]
    return url

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)

#From base url, get all navigation links
def get_nav_links(section_url):
    soup = make_soup(section_url)
    navs = soup.findAll('div', {'class': 'sub-nav__links'})
    links = []
    for nav in navs:
        links.extend([li.a['href'] for li in nav.findAll('li')])
    return links

# From all navigation links, find all links for events and exhibitions
def get_link_events(link_url):
    soup = make_soup(link_url)
    if 'exhibitions' in link_url:
        elems = soup.findAll('div', {'class': 'exhibition-row__details'})
    else:
        events_list = soup.find('div', {'id': 'events_list'})
        elems = events_list.findAll('h2', {'class': 'event__title'})
    return [elem.a['href'] for elem in elems]

# From current exhibition links, get relevant title, dates, and information
def get_event_info(event_url):
    soup = make_soup(event_url)

    if 'exhibitions' in event_url:
        title = soup.find('h1', {'class': 'exhibition__title'}).text.strip()
        date = soup.find('time', {'class': 'exhibition__date'}).text.strip()
        # Harvard broke the main image, so just get the thumbnail slideshow
        img_elem = soup.find('div', {'class': 'slideshow-thumbs__thumbs'})
        image = strip_args(img_elem.img['src']) if img_elem is not None else ""
        loc = soup.find('span', {'class': 'exhibition__host'}).text.strip()
        innerHTML = soup.find('div', {'class': 'exhibition__inner'})
        text = '\n\n'.join([i.text.strip() for i in innerHTML.findAll('p')])

    else:
        title = soup.find('h1', {'class': 'detail-page__title'}).text.strip()
        date = soup.find('time', {'class': 'detail-page__meta'}).text.strip()
        time = soup.find('p', {'class': 'detail-page__type'}).time.text.strip()
        date = date + " " + time
        loc = soup.find('p', {'class': 'vcard'}).find('span', {'class': 'fn'}).text.strip()

        hero_elem = soup.find('figure', {'class': 'detail-page__hero'})
        image = hero_elem.img['src'] if hero_elem is not None else ""

        innerHTML = soup.find('div', {'class': 'detail-page__inner'})
        text = '\n\n'.join([i.text.strip() for i in innerHTML.findAll('p', {'class': None})])

    return title, date, loc, text, image


###############################
#### Get events information from Harvard Art Museums website
#### Currently, all information for the event is captured

def scrape():
    allEvents = [] #List for all dictionaries

    links = get_nav_links(BASE_URL) #get all navigation links from main page

    events = []
    for link in links:
        if re.match('(.*)(exhibitions|calendar)', link, re.I): #find the calendar link
            events.extend(get_link_events(link)) #all exhibition links

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
