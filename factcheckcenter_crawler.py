# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash,db_init,db_update
import time
import hashlib


base = 'https://tfc-taiwan.org.tw'

media = '台灣事實查核中心'

#db initialization
collection = db_init(media)

soup = get_page("https://tfc-taiwan.org.tw/articles/report")
titles = soup.find_all('div', class_='view-content')[0].find_all('h3')

urls = []
for title in titles:
	url_temp = base + title.find('a')['href']
	urls.append(url_temp)

article_count = 0
for url in urls:
	soup = get_page(url)
	try:
		category = soup.find('div','field-name-field-taxo-report-attr').text.strip()
		title = soup.find('h2', 'node-title').text
		para = soup.find('div', 'field field-name-body field-type-text-with-summary field-label-hidden').find_all(['p','h2']) #get headings and content
		content = []
		content_str = ""
		content_str += title
		for p in para:
			content.append(p.text)
			content_str+=p.text
		tags = []
		modified_date = soup.find('div', 'submitted').text

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
		print("台灣事實查核中心 factcheckcenter")
		print(url)
		print(e)
		continue
