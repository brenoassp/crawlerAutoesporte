from bs4 import BeautifulSoup
from urllib.request import urlopen

def url_to_be_crawled():
	return "http://revistaautoesporte.globo.com/rss/ultimas/feed.xml"

def get_items():
	html = urlopen(url_to_be_crawled())
	bs = BeautifulSoup(html, "lxml-xml")
	items = bs.findAll("item")
	return items

def get_dict_item_list():
	items = get_items()
	l = []
	for item in items:
		d = {}
		d["title"] = item.find("title").contents[0]
		d["link"] = item.find("link").contents[0]
		content = []
		c = {}
		l.append(d)
	return l

def get_titles_xml():
	items = get_items()
	titles = []
	for item in items:
		titles.append(item.find("title").contents[0])
	return titles

def get_urls():
	items = get_items()
	urls = []
	for item in items:
		urls.append(item.find("link").contents[0])
	return urls

if __name__ == '__main__':
	items = get_items()
	for item in get_items():
		tmp = item.find("description").contents[0]
		z = BeautifulSoup(tmp)
		print(z.findAll("p"))
		break
		print(item.find("description").contents[0].findAll("p"))
		break