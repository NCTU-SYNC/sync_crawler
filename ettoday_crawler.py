# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash,db_init,db_update
import time
import hashlib

base = "https://www.ettoday.net"

media = 'ettoday'

#db initialization
collection = db_init(media)

soup = get_page("https://www.ettoday.net/news/news-list.htm")
sel = soup.find('div', 'part_list_2').find_all('h3')
article_count = 0

for s in sel:
	modified_date = s.find('span').text	
	category = s.find('em').text
	url = base + s.find('a')['href']
	try:
		soup = get_page(url)
		title = soup.find('h1', 'title').text

		article_content = []
		content_str = ""
		content_str += title
		tags = []
		for p in soup.find('div','story').find_all('p'):
			pText = p.text
			
			if '►' in pText or '▲' in pText or '·' in pText or pText == '' or '▼' in pText:
				continue
			if '更多鏡週刊報導' in pText or '你可能也想看' in pText or '其他新聞' in pText or '其他人也看了' in pText or '更多新聞' in pText:
				break
			
			article_content.append(p.text)
			content_str += p.text
			
		#find tags
		tags = soup.find("meta",attrs={"name": "news_keywords"}).attrs['content'].split(',')

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

		article_count+=1
		#if article_count >= 50:
		#	break

	except Exception as e:
		print("ETtoday")
		print(url)
		print(e)
		continue
