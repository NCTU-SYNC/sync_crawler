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


url = {}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

text_club = "蘭姆酒吐司"
md = hashlib.md5()

r = requests.get("https://www.rumtoast.com/%E5%88%86%E9%A1%9E/%e8%98%ad%e5%a7%86%e9%85%92%e5%90%90%e5%8f%b8", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find_all('div', 'td-module-thumb')
count = 0
for s in sel:
	url[count] = s.find('a')['href']
	count+=1	
for u in url:
	r = requests.get(url[u], headers = headers)#get HTML
	r.encoding='UTF-8'
	soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
	try:
		category = []
		cat_temp = soup.find('ul', 'td-category').find_all('li')
		for c in cat_temp:
			category.append(c.text)
		title = soup.find('h1', 'entry-title').text
		sel = soup.find('div', 'td-post-content').find_all('p')
		content = []
		tag = []
		for s in sel:
			content.append(s.text)
		date = soup.find('span', 'td-post-date').text
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
		print("蘭姆酒吐司")
		print(url[u])
		print(e)
		continue