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



url = "https://www.ettoday.net/"
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

text_club = "ettoday"
md = hashlib.md5()
ai = 1

r = requests.get("https://www.ettoday.net/news/news-list.htm", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find('div', 'part_list_2').find_all('h3')
for s in sel:
	date = s.find('span').text	
	category = s.find('em').text
	u = url + s.find('a')['href']
	try:
		r = requests.get(u)#get HTML
		r.encoding='UTF-8'
		soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
		title = soup.find('h1', 'title').text	
		content = ""
		tag = ""
		for p in soup.find('div','story').find_all('p'):
			content+=(p.text)
		md.update((str)(title+date+text_club).encode('utf-8'))                   #制定需要加密的字符串
		news_dict['id'] = md.hexdigest()
		news_dict['title'] = title
		news_dict['content'] = content
		news_dict['category'] = category
		news_dict['date'] = date
		news_dict['news_club'] = text_club
		news_dict['tag'] = tag
		news_dict['url'] = u
	
		# print(news_dict)
		# print("\naaaaaaaaaaaaaaaaaaaaaaaa\n\n")

		# mongodb.logindb();
		# x = collection.update_many({"id": news_dict['id']}, {"$set": news_dict}, upsert=True)
	except Exception as e:
		print("ETtoday")
		print(u)
		print(e)
		continue
