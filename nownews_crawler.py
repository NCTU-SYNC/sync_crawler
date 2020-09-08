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



url = []
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

text_club = "Nownews"
md = hashlib.md5()
def get_one_page():
    try:
        response = requests.get("https://www.nownews.com/WirelessFidelity/staticFiles/nownewsIndexpage/indexpageCacheJson",headers=headers)
        if response.status_code == 200:
        	return response.json()##将返回的json数据转换为python可读的字典数据,.json是requests库自带的函数。
        return None
    except Exception as e:
        print("抓取失败")


def parse_data():
	first = True
	data = get_one_page()
	# print(data)
	for x in data:
		url.append(x["link"])							
parse_data()
# first = True
for u in url:
	try:
		r = requests.get(u, headers = headers)#get HTML
		r.encoding='UTF-8'
		soup = BeautifulSoup(r.text,"html.parser")
		content = ""
		tag = ""
		temp = soup.find('title').text
		title = temp.split('|', 1)[0]
		category = temp.split('|', 2)[1]
		sel = soup.find('div', 'td-post-content').find_all('p')
		for p in sel:
			try:
				str123 = p['class']
			except:	
				content+=p.text
		sel = soup.find('ul', 'td-tags td-post-small-box clearfix').find_all('li')
		for p in sel:
			tag+=("#"+p.text)			
		date = soup.find('span', 'reynold_updateTime').text
		md.update((str)(title+date+text_club).encode('utf-8'))                  #制定需要加密的字符串
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

		mongodb.logindb();
		x = collection.update_many({"id": news_dict['id']}, {"$set": news_dict}, upsert=True)	
	except Exception as e:
		print("nownews")
		print(e)
		continue
			
