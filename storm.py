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



url = {}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

text_club = "風傳媒"
md = hashlib.md5()
ai = 1

r = requests.get("https://www.storm.mg/articles", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find_all('div', 'category_card card_thumbs_left')
count = 0
for s in sel:
	url[count] = s.find('a')['href']
	# if count!=0 and count!=len(sel)-1:
	# 	url[sel[count].text] = sel[count].find('a')['href']
	# if count==len(sel)-1:
	# 	sel = sel[count].find_all('a', onclick = True)
	# 	i = 0
	# 	for se in sel:
	# 		if i!=len(sel)-1:
	# 			url[sel[i].text] = sel[i]['href']
	# 		i+=1	
	count+=1
# print(url)	
first = True
for u in url:
	category = []
	try:
		r = requests.get(url[u])#get HTML
		r.encoding='UTF-8'
		soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
		sel = soup.find('div', id = 'title_tags_wrapper')
		for s in sel.find_all('a'):
			category.append(s.get_text())
		title = soup.find('h1', id = 'article_title').text	
		content = ""
		tag = ""
		for p in soup.find('div', id = 'CMS_wrapper').find_all('p'):
			content+=(p.text)
		date = soup.find('span', 'info_time').text
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

		mongodb.logindb();
		x = collection.update_many({"id": news_dict['id']}, {"$set": news_dict}, upsert=True)
	except Exception as e:
		print("風傳媒storm")
		print(e)
		continue
