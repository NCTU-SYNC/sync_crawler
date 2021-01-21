# -!- coding: utf-8 -!-
import requests
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

media = "中央社"

r = requests.get("https://www.cna.com.tw/list/aall.aspx", headers = headers)#get HTML
r.encoding='UTF-8'
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.find('ul', 'mainList imgModule', id = 'jsMainList').find_all('li')

#add each url to url list
count = 0
for s in sel:
	url[count] = s.find('a')['href']
	count+=1

newscount = 0
for u in url:
	r = requests.get(url[u], headers = headers)#get HTML
	r.encoding='UTF-8'
	soup = BeautifulSoup(r.text,"html.parser")
	try:
		category = soup.find('div', 'breadcrumb').find_all('a')[1].text
		title = soup.find('div', 'centralContent').find('h1').text
		sel = soup.find('div', 'paragraph').find_all('p')
		article_content = []
		content = ""
		tags = []
		for s in  sel:
			content+=s.text
			article_content.append(s.text)

		date = soup.find('div', 'updatetime').find('span').text
		
		news_dict['id'] = newscount #hash -> need to change
		news_dict['title'] = title
		news_dict['content'] = article_content
		news_dict['category'] = category
		news_dict['pubdate'] = date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url[u]
		newscount+=1
		
		print(news_dict) #insert to db, currently print
		
	except Exception as e:
		print("中央社cna")
		print(url[u])
		print(e)
		continue