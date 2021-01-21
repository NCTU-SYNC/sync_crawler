# -!- coding: utf-8 -!-
import requests
import csv
from bs4 import BeautifulSoup
import time
import codecs
from os import listdir
from os.path import isfile, isdir, join
# encoding:utf-8
import json
import hashlib


url_base = "https://news.ebc.net.tw/"
url = {}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

media = "東森"
md = hashlib.md5()

r = requests.get("https://news.ebc.net.tw/realtime", headers = headers) #get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find('div', 'news-list-box').find_all('div', 'style1 white-box') #get news list
count = 0
for s in sel:
	url[count] = url_base + s.find('a')['href']
	count+=1	
print(count)
count = 0			
for u in url:
	r = requests.get(url[u], headers = headers)#get HTML
	r.encoding='UTF-8'
	soup = BeautifulSoup(r.text,"html.parser")
	try:
		category = soup.find('div', id = 'web-map').find_all('a')[1].text
		title = soup.find('div', 'fncnews-content').find('h1').text

		content_sel = soup.find('div', 'raw-style').find_all('p')
		article_content = []
		for p in content_sel:
			content = p.text
			#clear unwanted content
			if content.startswith('★') or not content or '延伸閱讀' in content:
				continue
			if '\u3000' in content:
				content.replace('\u3000',' ')
			if '\xa0' == content:
				continue			
			article_content.append(content.strip())
		
		tags = []
		try:
			sel = soup.find('div', 'keyword').find_all('a')
			for s in sel:
				tags.append(s.text)
		except:
			tags = []		
		date = soup.find('span', 'small-gray-text').text
		
		news_dict['id'] = count
		news_dict['title'] = title
		news_dict['content'] = article_content
		news_dict['category'] = category
		news_dict['pubdate'] = date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url[u]
		print(news_dict)

		count += 1

	except Exception as e:
		print("東森ebc")
		print(url[u])
		print(e)
		continue