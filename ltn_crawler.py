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


urls = []
url_title = ["https://news.ltn.com.tw/ajax/breakingnews/all/1", "https://news.ltn.com.tw/ajax/breakingnews/all/2", "https://news.ltn.com.tw/ajax/breakingnews/all/3"]
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
def get_one_page(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
        	return response.json()##将返回的json数据转换为python可读的字典数据,.json是requests库自带的函数。
        return None
    except :
        print("抓取失败")

def parse_data():
	first = True
	count = 20
	for url in url_title:
		data = get_one_page(url)
		if first:
			for url in data['data']:
				urls.append(url['url'])	
		else:
			for i in range(20):
				number = str(count)
				urls.append(data['data'][number]['url'])
				count+=1
		first = False									
parse_data()
news_dict = {}

text_club = "自由時報"
md = hashlib.md5()

# r = requests.get(urls[0], headers = headers)#get HTML
# r.encoding='UTF-8'
# soup = BeautifulSoup(r.text,"html.parser")
# title = soup.find('h1').text
# # print(title)
# content = ""
# tag = ""
# for p in soup.find('div', 'text boxTitle boxText').find_all('p'):
# 	print(p)
# # 	print("#########")
# # 	content+=(p.text)
# # print(content)	
# date = soup.find('span', 'time').text
for u in urls:
	try:
		r = requests.get(u, headers = headers)#get HTML
		r.encoding='UTF-8'
		soup = BeautifulSoup(r.text,"html.parser")
		title = soup.find('h1').text
		# print(title)
		content = ""
		content_temp = ""
		tag = ""
		for p in soup.find('div', 'text boxTitle boxText').find_all('p'):
			content = content_temp
			content_temp+=(p.text)
		category = 	soup.find('div', 'breadcrumbs boxTitle boxText').text
		category = 	category[6:]
		date = soup.find('span', 'time').text
		date.lstrip()
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

		mongodb.logindb();
		x = collection.update_many({"id": news_dict['id']}, {"$set": news_dict}, upsert=True)
	except Exception as e:
		print("自由時報ltn")
		print(u)
		print(e)
		continue