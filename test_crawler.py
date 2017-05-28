import pytest
import crawler
from urllib.request import urlopen
from urllib.error import HTTPError

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

def test_dict_items_have_correct_structure():
	dict_items = crawler.get_dict_item_list()
	for dict_item in dict_items:
		assert "title" in dict_item
		assert "link" in dict_item
		assert "content" in dict_item

def test_dict_item_titles_is_equal_to_xml_titles():
	dict_item_list = crawler.get_dict_item_list()
	dict_item_titles = []
	for d in dict_item_list:
		dict_item_titles.append(d["title"])
	titles_dict_items_set = set(dict_item_titles)
	titles_xml_set = set(crawler.get_titles_xml())

	assert len(titles_dict_items_set.symmetric_difference(titles_xml_set)) == 0