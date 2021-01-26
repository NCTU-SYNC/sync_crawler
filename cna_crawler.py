# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash,db_init,db_update
import time
import hashlib

media = '中央社'

#db initialization
collection = db_init(media)

soup = get_page('https://www.cna.com.tw/list/aall.aspx')
sel = soup.find('ul', 'mainList imgModule', id = 'jsMainList').find_all('li')

#add each url to url list
urls = []
for s in sel:
	urls.append(s.find('a')['href'])

news_count = 0
for url in urls:
	soup = get_page(url)
	try:
		category = soup.find('div', 'breadcrumb').find_all('a')[1].text
		title = soup.find('div', 'centralContent').find('h1').text
		sel = soup.find('div', 'paragraph').find_all('p')
		article_content = []
		content_str = ""
		content_str += title
		tags = []
		for s in sel:
			article_content.append(s.text)
			content_str += s.text

		modified_date = soup.find('meta',itemprop='dateModified')['content']
		
		url_hash = generate_hash(url)
		content_hash = generate_hash(content_str)

		news_dict = {}
		news_dict['title'] = title
		news_dict['content'] = article_content
		news_dict['category'] = category
		news_dict['modified_date'] = modified_date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url
		news_dict['url_hash'] = url_hash
		news_dict['content_hash'] = content_hash
		
		db_update(collection,news_dict)
		print(news_dict)
		
		news_count+=1
		#Default is 100
		if news_count == 50:
			break
		
	except Exception as e:
		print("中央社cna")
		print(url)
		print(e)
		continue