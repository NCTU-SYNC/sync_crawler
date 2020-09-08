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
import mongodb
from mongodb import collection

import hashlib


url_base = "https://news.ebc.net.tw/"
url = {}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

text_club = "東森"
md = hashlib.md5()
ai = 1

r = requests.get("https://news.ebc.net.tw/realtime", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find('div', 'news-list-box').find_all('div', 'style1 white-box')
count = 0
for s in sel:
	url[count] = url_base + s.find('a')['href']
	count+=1				
for u in url:
	r = requests.get(url[u], headers = headers)#get HTML
	r.encoding='UTF-8'
	soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
	try:
		category = soup.find('div', id = 'web-map').find_all('a')[1].text
		title = soup.find('div', 'fncnews-content').find('h1').text
		content = soup.find('div', 'raw-style').find('span').text
		tag = []
		try:
			sel = soup.find('div', 'keyword').find_all('a')
			for s in sel:
				tag.append(s.text)
		except:
			tag = []		
		date = soup.find('span', 'small-gray-text').text
		md.update((str)(title+date+text_club).encode('utf-8'))                   #制定需要加密的字符串
		news_dict['id'] = md.hexdigest()
		news_dict['title'] = title
		news_dict['content'] = content
		news_dict['category'] = category
		news_dict['date'] = date
		news_dict['news_club'] = text_club
		news_dict['tag'] = tag
		news_dict['url'] = url[u]
		print(news_dict)
		print("\naaaaaaaaaaaaaaaaaaaaaaaa\n\n")

		# mongodb.logindb();
		# x = collection.update_many({"id": news_dict['id']}, {"$set": news_dict}, upsert=True)
	except Exception as e:
		print("東森ebc")
		print(url[u])
		print(e)
		continue