# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page
import time
import json
import hashlib



urls = []
news_dict = {}

media = "風傳媒"

soup = get_page("https://www.storm.mg/articles")
sel = soup.find_all('div', 'category_card card_thumbs_left')

for s in sel:
	urls.append(s.find('a')['href'])

count = 0
for url in urls:
	category = []
	try:
		soup = get_page(url)
		sel = soup.find('div', id = 'title_tags_wrapper')
		for s in sel.find_all('a'):
			category.append(s.get_text())
		title = soup.find('h1', id = 'article_title').text	
		content = []
		tags = []
		for p in soup.find('div', id = 'CMS_wrapper').find_all('p'):
			content.append(p.text)
		pubdate = soup.find('span', id = 'info_time').text
		
		news_dict['id'] = count
		news_dict['title'] = title
		news_dict['content'] = content
		news_dict['category'] = category
		news_dict['pubdate'] = pubdate
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url
	
		print(news_dict)
		count+=1
	except Exception as e:
		print("風傳媒storm")
		print(url)
		print(e)
		continue
