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

text_club = "tvbs"
md = hashlib.md5()
ai = 1

r = requests.get("https://news.tvbs.com.tw/", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find('div', 'header_menu_nav')
sel = sel.find_all('li')
count = 0
for s in sel:
	if count!=0 and count!=len(sel)-1:
		url[sel[count].text] = sel[count].find('a')['href']
	if count==len(sel)-1:
		sel = sel[count].find_all('a', onclick = True)
		i = 0
		for se in sel:
			if i!=len(sel)-1:
				url[sel[i].text] = sel[i]['href']
			i+=1	
	count+=1
for u in url:
	r.encoding='UTF-8'
	soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
	sel = soup.find('div', 'content_center_list_box')
	try:
		sel = sel.find_all('a')
		category = u
		for s in sel:
			gurl = 'https://news.tvbs.com.tw'
			gurl += s['href']
			n = requests.get(gurl, headers = headers)#get HTML
			n.encoding='UTF-8'
			soup2 = BeautifulSoup(n.text,"html.parser") #將網頁資料以html.parser
			title = soup2.find('h1', 'margin_b20').text
			sel2 = soup2.find_all('div', id = 'news_detail_div')
			content = ""
			tag = ""
			content = sel2[0].text
			sel_tag =  soup2.find('div', 'adWords')
			for t in sel_tag.find_all('a'):
				tag+=("#"+t.text)	
			date = soup2.find('div', 'icon_time').text
			md.update((str)(title+date+text_club).encode('utf-8'))                   #制定需要加密的字符串
			news_dict['id'] = md.hexdigest()
			news_dict['title'] = title
			news_dict['content'] = content
			news_dict['category'] = category
			news_dict['date'] = date
			news_dict['news_club'] = text_club
			news_dict['tag'] = tag
			news_dict['url'] = gurl
	
			# print(news_dict)
			# print("\naaaaaaaaaaaaaaaaaaaaaaaa\n\n")

			mongodb.logindb();
			x = collection.update_many({"id": news_dict['id']}, {"$set": news_dict}, upsert=True)
	except:	
		continue
