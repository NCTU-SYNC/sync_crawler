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


url_title = 'https://tfc-taiwan.org.tw/'
url = {}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

media = "台灣事實查核中心"
md = hashlib.md5()

r = requests.get("https://tfc-taiwan.org.tw/articles/report", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
titles = soup.find_all('div', class_='view-content')[0].find_all('h3')
count = 0

for title in titles:
	url_temp = url_title + title.find('a')['href']
	url[count] = url_temp
	count+=1
	
for u in url:
	r = requests.get(url[u], headers = headers)#get HTML
	r.encoding='UTF-8'
	soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
	try:
		category = soup.find('div','field-name-field-taxo-report-attr').text.strip()
		title = soup.find('h2', 'node-title').text
		para = soup.find('div', 'field field-name-body field-type-text-with-summary field-label-hidden').find_all(['p','h2']) #get headings and content
		content = []
		for p in para:
			content.append(p.text)
		tags = []
		date = soup.find('div', 'submitted').text

		news_dict['id'] = u #need to fix
		news_dict['title'] = title
		news_dict['content'] = content
		news_dict['category'] = category
		news_dict['pubdate'] = date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url[u]
		print(news_dict)
		
	except Exception as e:
		print("台灣事實查核中心")
		print(url[u])
		print(e)
		continue
