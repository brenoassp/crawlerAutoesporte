import pytest
import crawler
from urllib.request import urlopen
from urllib.error import HTTPError
import random
import datetime
from bs4 import BeautifulSoup

def test_page_was_successfully_opened():
	urlopen(crawler.url_to_be_crawled())

def test_gotten_titles_are_correct():
	some_titles_set = set(['Donald Trump quer impedir vendas de carros alemães nos EUA',
					'Hyundai lança série de vídeos teaser do SUV Kona',
					'Fiat Argo tem cadastro para test drive e primeira promoção',
					'Chevrolet Prisma 2018 chega com novos itens, mas mais caro'])
	gotten_titles = crawler.get_titles_xml()

	assert type(gotten_titles) is list
	assert len(gotten_titles) > 0

	gotten_titles_set = set(gotten_titles)

	assert some_titles_set.issubset(gotten_titles_set)

def test_gotten_links_are_correct():
	some_urls_set = set(['http://revistaautoesporte.globo.com/Noticias/noticia/2017/05/donald-trump-quer-impedir-vendas-de-carros-alemaes-nos-eua.html',
					'http://revistaautoesporte.globo.com/Noticias/noticia/2017/05/fiat-argo-tem-cadastro-para-test-drive-e-primeira-promocao.html',
					'http://revistaautoesporte.globo.com/Noticias/noticia/2017/05/tudo-sobre-o-evento-qual-comprar-2017.html'])
	gotten_urls = crawler.get_urls()

	assert type(gotten_urls) is list
	assert len(gotten_urls) > 0

	gotten_urls_set = set(gotten_urls)

	assert some_urls_set.issubset(gotten_urls_set)

def test_dict_item_titles_is_equal_to_xml_titles():
	dict_item_list = crawler.get_dict_item_list()
	dict_item_titles = []
	for d in dict_item_list:
		dict_item_titles.append(d["title"])
	titles_dict_items_set = set(dict_item_titles)
	titles_xml_set = set(crawler.get_titles_xml())

	assert len(titles_dict_items_set.symmetric_difference(titles_xml_set)) == 0

def test_div_contains_class_foto():
	soup = BeautifulSoup('<div></div>', "html.parser")

	assert crawler.is_div_that_contains_img(soup.div) == False

	soup = BeautifulSoup('<div><img alt="zzz"></img></div>', "html.parser")

	assert crawler.is_div_that_contains_img(soup.div) == True

def test_tag_is_paragraph():
	soup = BeautifulSoup('<div><p></p></div>', "html.parser")

	assert crawler.is_paragraph(soup.div) == False

	assert crawler.is_paragraph(soup.p) == True

def test_div_that_contains_links():
	soup = BeautifulSoup('<div><p></p></div>', "html.parser")

	assert crawler.is_div_that_contains_links(soup.div) == False

	soup = BeautifulSoup('<div class="saibamais"></div>', "html.parser")

	assert crawler.is_div_that_contains_links(soup.div) == True

def test_paragraph_is_empty():
	soup = BeautifulSoup('<div><p></p></div>', "html.parser")

	assert crawler.paragraph_is_empty(soup.p) == True

	soup = BeautifulSoup('<div><p>zzz</p></div>', "html.parser")

	assert crawler.paragraph_is_empty(soup) == False

def test_get_dict_by_item():
	random.seed(datetime.datetime.now())
	items = crawler.get_items()
	item = items[random.randint(0, len(items)-1)]
	d = crawler.get_dict_by_item(item)

	assert "title" in d

	assert "link" in d

	assert type(d["content"]) is list

	assert len(d["content"]) > 0

	for c in d["content"]:
		assert "type" in c
		assert "content" in c
		assert "image" or "text" or "links" in c

def test_dict_items_have_correct_structure():
	dict_item_list = crawler.get_dict_item_list()
	random.seed(datetime.datetime.now())
	for i in range(0,5):
		index_of_item_to_be_tested = random.randint(0, len(dict_item_list)-1)
		assert "title" in dict_item_list[index_of_item_to_be_tested]
		assert "link" in dict_item_list[index_of_item_to_be_tested]
		assert "content" in dict_item_list[index_of_item_to_be_tested]
		assert type(dict_item_list[index_of_item_to_be_tested]["content"]) is list
		for j in range(0,3):
			index_of_content_to_be_tested = random.randint(0, len(dict_item_list[index_of_item_to_be_tested]["content"]))
			assert "type" in dict_item_list[index_of_item_to_be_tested]["content"][index_of_content_to_be_tested]
			assert "content" in dict_item_list[index_of_item_to_be_tested]["content"][index_of_content_to_be_tested]
			possible_type_set = set(["image", "text", "links"])
			type_current_item_set = set([dict_item_list[index_of_item_to_be_tested]["content"][index_of_content_to_be_tested]["type"]])
			assert type_current_item_set.issubset(possible_type_set)
