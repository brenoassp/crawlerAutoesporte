from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from urllib.request import urlopen
import json

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
		l.append(get_dict_by_item(item))
	return l

def get_titles_xml():
	items = get_items()
	titles = []
	for item in items:
		titles.append(get_title(item))
	return titles

def get_urls():
	items = get_items()
	urls = []
	for item in items:
		urls.append(get_link(item))
	return urls

def is_tag(tag):
	if type(tag) is Tag:
		return True
	return False

def is_div_that_contains_img(tag):
	return tag.img is not None

def is_paragraph(tag):
	return tag.name == "p"

def paragraph_is_empty(tag):
	l = list(tag.stripped_strings)
	return len(l) == 0

def is_div_that_contains_links(tag):
	return "class" in tag.attrs and "saibamais" in tag.attrs["class"]

def get_title(item):
	return item.find("title").contents[0]

def get_link(item):
	return item.find("link").contents[0]

def get_paragraph_text_without_blank_spaces(tag):
	if not is_tag(tag):
		raise TypeError("Argument provided is not a tag")
	if not is_paragraph(tag):
		raise ValueError("Tag provided is not a paragraph")
	list_strings = list(tag.stripped_strings)
	content = ""
	for string in list_strings:
		content += " " + string
	content = content[1:]
	return content

def get_dict_by_item(item):
	dict_item = {}
	dict_item["title"] = get_title(item)
	dict_item["link"] = get_link(item)
	dict_item["content"] = []

	list_dict_contents = []
	description_html = BeautifulSoup(item.find("description").contents[0], "html.parser")
	first = description_html.find("div", {"class":"foto"})
	tags_not_empty_paragraphs = []
	tags_not_empty_paragraphs.append(first)
	for s in first.next_siblings:
		if not is_tag(s):
			continue
		if not is_paragraph(s):
			tags_not_empty_paragraphs.append(s)
		elif not paragraph_is_empty(s):
			tags_not_empty_paragraphs.append(s)

	for i in tags_not_empty_paragraphs:
		d = {}
		if is_paragraph(i):
			d["type"] = "text"
			d["content"] = get_paragraph_text_without_blank_spaces(i)
			dict_item["content"].append(d)
		elif is_div_that_contains_img(i):
			d["type"] = "image"
			d["content"] = i.img.attrs["src"]
			dict_item["content"].append(d)
		elif is_div_that_contains_links(i):
			d["type"] = "links"
			d["content"] = []
			for link in i.findAll("a"):
				d["content"].append(link.attrs["href"])
			dict_item["content"].append(d)
	return dict_item

if __name__ == '__main__':
	with open('data.txt', 'w') as outfile:
		for item in get_dict_item_list():
			json.dump(item, outfile, indent = 4, sort_keys=False, ensure_ascii=False)
			outfile.write("\n")