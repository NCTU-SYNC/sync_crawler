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



url = { '不分類' : 'https://udn.com/news/breaknews/1/99#breaknews'}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
# with codecs.open(timename, "r+", encoding = 'utf_8_sig') as csvFile:

#   # 讀取 CSV 檔案內容
#   rows = csv.reader(csvFile)

#   # 以迴圈輸出每一列
#   for row in rows:
#     print(row[1])
news_dict = {}
# with codecs.open(timename, "r+", encoding = 'utf_8_sig') as csvFile:

#   # 讀取 CSV 檔案內容
count = 0
#   # 以迴圈輸出每一列
# 	# for row in rows:
# 	# 	print(row[1])
# 	# count = int(len(csvFile.readlines()))-1
# 	# print(count)
# 	#定義欄位
# 	fieldNames = ['id', '標題', '內文']

# 	#將dictionary寫入CSV檔
# 	writer = csv.DictWriter(csvFile, fieldNames)

	# 寫入第一列的欄位名稱
	# writer.writeheader()
countflag = 0
text_club = "聯合"
md = hashlib.md5()
ai = 1
for u in  url:
	r = requests.get(url[u], headers = headers)#get HTML
	r.encoding='UTF-8'
	soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
	# str01 = "div.area_body"
	sel = soup.find_all('div', id = 'breaknews_body')
	sel = sel[0].find_all('dt')
	for s in sel:
		try:
			gurl = "https://udn.com/"
			gurl += s.find('a')['href']
			category = s.find('a', 'cate').text
			n = requests.get(gurl, headers = headers)#get HTML
			n.encoding='UTF-8'
			soup2 = BeautifulSoup(n.text,"html.parser") #將網頁資料以html.parser
			title = soup2.find('h1', 'story_art_title').text
			sel2 = soup2.find_all('div', id = 'story_body_content')
			content = ""
			tag = ""
			for p in sel2[0].find_all('p'):
				content+=(p.text)
			for p in soup2.find_all('div', id = 'story_tags'):
				for p2 in p.find_all('a'):
					tag+=("#"+p2.text)	
			date = soup2.find('div', 'story_bady_info_author')
			date = date.find('span').text
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
		except Exception as e:
			print("udn")
			print(e)
			continue