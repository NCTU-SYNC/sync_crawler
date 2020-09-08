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
#from mongodb import collection

import hashlib


url_title = 'https://tfc-taiwan.org.tw/'
url = {}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

text_club = "台灣事實查核中心"
md = hashlib.md5()

r = requests.get("https://tfc-taiwan.org.tw/articles/report", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find_all('div', 'views-row')
count = 0
for s in sel:
	url_temp = url_title + s.find('h3', 'article-title').find('a')['href']
	url[count] = url_temp
	count+=1
for u in url:
	r = requests.get(url[u], headers = headers)#get HTML
	r.encoding='UTF-8'
	soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
	try:
		category = soup.find('div', 'field-item odd').text
		title = soup.find('h3', 'article-title').text
		sel = soup.find('div', 'field field-name-body field-type-text-with-summary field-label-hidden').find_all('p')
		content = ""
		tag = ""
		for s in sel:
			content+=s.text	
		date = soup.find('div', 'grid_5').text
		md.update((str)(title+date+text_club).encode('utf-8'))                   #制定需要加密的字符串
		news_dict['id'] = md.hexdigest()
		news_dict['title'] = title
		news_dict['content'] = content
		news_dict['category'] = category
		news_dict['date'] = date
		news_dict['news_club'] = text_club
		news_dict['tag'] = tag
		news_dict['url'] = url[u]
		# print(news_dict)
		# print("\naaaaaaaaaaaaaaaaaaaaaaaa\n\n")

		collection = mongodb.logindbcheckfact();
		x = collection.update_many({"id": news_dict['id']}, {"$set": news_dict}, upsert=True)
	except Exception as e:
		print("台灣事實查核中心")
		print(url[u])
		print(e)
		continue