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



url = "https://www.ettoday.net/"
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

media = "ettoday"
md = hashlib.md5()
ai = 1

r = requests.get("https://www.ettoday.net/news/news-list.htm", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find('div', 'part_list_2').find_all('h3')
count = 0
for s in sel:
	date = s.find('span').text	
	category = s.find('em').text
	u = url + s.find('a')['href']
	try:
		r = requests.get(u)#get HTML
		r.encoding='UTF-8'
		soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
		title = soup.find('h1', 'title').text
		#print(title,u)
		content = []
		tags = []
		for p in soup.find('div','story').find_all('p'):
			pText = p.text
			
			if '►' in pText or '▲' in pText or '·' in pText or pText == '' or '▼' in pText:
				continue
			if '更多鏡週刊報導' in pText or '你可能也想看' in pText or '其他新聞' in pText or '其他人也看了' in pText or '更多新聞' in pText:
				break
			
			content.append(p.text)
		#find tags
		tags = soup.find("meta",attrs={"name": "news_keywords"}).attrs['content'].split(',')
		#print(test[])
		news_dict['id'] = count
		news_dict['title'] = title
		news_dict['content'] = content
		news_dict['category'] = category
		news_dict['pubdate'] = date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = u
		
		print(news_dict)

		count+=1
		if count >= 50:
			break

	except Exception as e:
		print("ETtoday")
		print(u)
		print(e)
		continue
