# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page
import time
import hashlib


base = 'https://tfc-taiwan.org.tw/'
urls = []
news_dict = {}

media = "台灣事實查核中心"
md = hashlib.md5()

soup = get_page("https://tfc-taiwan.org.tw/articles/report")
titles = soup.find_all('div', class_='view-content')[0].find_all('h3')

for title in titles:
	url_temp = base + title.find('a')['href']
	urls.append(url_temp)

count = 0
for url in urls:
	soup = get_page(url)
	try:
		category = soup.find('div','field-name-field-taxo-report-attr').text.strip()
		title = soup.find('h2', 'node-title').text
		para = soup.find('div', 'field field-name-body field-type-text-with-summary field-label-hidden').find_all(['p','h2']) #get headings and content
		content = []
		for p in para:
			content.append(p.text)
		tags = []
		date = soup.find('div', 'submitted').text

		news_dict['id'] = count #need to fix
		news_dict['title'] = title
		news_dict['content'] = content
		news_dict['category'] = category
		news_dict['pubdate'] = date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url
		print(news_dict)
		count+=1
		
	except Exception as e:
		print("台灣事實查核中心")
		print(url)
		print(e)
		continue
