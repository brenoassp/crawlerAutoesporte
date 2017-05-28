from bs4 import BeautifulSoup
from urllib.request import urlopen

def url_to_be_crawled():
	return "http://revistaautoesporte.globo.com/rss/ultimas/feed.xml"

def getTitles():
	html = urlopen(url_to_be_crawled())
	bs = BeautifulSoup(html, "html.parser")
	items = bs.findAll("item")
	titles = []
	for item in items:
		titles.append(item.find("title").contents[0])
	return titles		

if __name__ == '__main__':
	html = urlopen(url_to_be_crawled())
	bs = BeautifulSoup(html, "html.parser")	


	for title in titles:
		print(title)
	'''tags = materias.findAll("title")
	titles = []
	for tag in tags:
		titles.append(tag.contents[0])
	print(titles)'''