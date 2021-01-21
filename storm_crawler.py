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



url = {}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

media = "風傳媒"
#md = hashlib.md5()

r = requests.get("https://www.storm.mg/articles", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find_all('div', 'category_card card_thumbs_left')
count = 0
for s in sel:
	url[count] = s.find('a')['href']	
	count+=1
count = 0
for u in url:
	category = []
	try:
		r = requests.get(url[u])#get HTML
		r.encoding='UTF-8'
		soup = BeautifulSoup(r.text,"html.parser")
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
		news_dict['url'] = url[u]
	
		print(news_dict)
		
	except Exception as e:
		print("風傳媒storm")
		print(e)
		continue
