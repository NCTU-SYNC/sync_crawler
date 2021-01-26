# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash,db_init,db_update
import time
import hashlib

urls = []
media = "風傳媒"

#db initialization
collection = db_init(media)

soup = get_page("https://www.storm.mg/articles")
sel = soup.find_all('div', 'category_card card_thumbs_left')

for s in sel:
	urls.append(s.find('a')['href'])

article_count = 0
for url in urls:
	category = []
	try:
		soup = get_page(url)
		sel = soup.find('div', id = 'title_tags_wrapper')
		for s in sel.find_all('a'):
			category.append(s.get_text())
		title = soup.find('h1', id = 'article_title').text	
		content = []
		content_str = ""
		content_str += title
		tags = []
		for p in soup.find('div', id = 'CMS_wrapper').find_all('p'):
			content.append(p.text)
			content_str += p.text
		modified_date = soup.find('span', id = 'info_time').text
		
		url_hash = generate_hash(url)
		content_hash = generate_hash(content_str)

		news_dict = {}
		news_dict['title'] = title
		news_dict['content'] = content
		news_dict['category'] = category
		news_dict['modified_date'] = modified_date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url
		news_dict['url_hash'] = url_hash
		news_dict['content_hash'] = content_hash

		db_update(collection,news_dict)
		print(news_dict)
		article_count+=1

	except Exception as e:
		print("風傳媒storm")
		print(url)
		print(e)
		continue
