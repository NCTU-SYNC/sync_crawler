# -!- coding: utf-8 -!-
import requests
import csv
from bs4 import BeautifulSoup
###from firebase import firebase
import time
import codecs
from os import listdir
from os.path import isfile, isdir, join
# encoding:utf-8
import json
import mongodb
from mongodb import collection

import hashlib

import datetime



url = { '即時' : 'https://news.cts.com.tw/real/index.html', '氣象': 'https://news.cts.com.tw/weather/index.html', '反送中': 'https://news.cts.com.tw/politics/index.html', '藝文': 'https://news.cts.com.tw/arts/index.html', '娛樂': 'https://news.cts.com.tw/entertain/index.html', '運動': 'https://news.cts.com.tw/sports/index.html', '生活': 'https://news.cts.com.tw/life/index.html', '財經': 'https://news.cts.com.tw/money/index.html', '台語': 'https://news.cts.com.tw/taiwanese/index.html', '地方': 'https://news.cts.com.tw/local/index.html', '校園': 'https://news.cts.com.tw/campus/index.html', '綜合': 'https://news.cts.com.tw/general/index.html', '國際': 'https://news.cts.com.tw/international/index.html', '社會': 'https://news.cts.com.tw/society/index.html'}
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
text_club = "華視"
md = hashlib.md5()
try:
	for u in  url:
		r = requests.get(url[u], headers = headers)#get HTML
		r.encoding='UTF-8'
		soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
		str01 = "div.newslist-container"
		sel = soup.select(str01)
		for s in sel[0].find_all('a', href=True):
			gurl = s['href']
			n = requests.get(gurl, headers = headers)#get HTML
			n.encoding='UTF-8'
			soup2 = BeautifulSoup(n.text,"html.parser") #將網頁資料以html.parser
			str02 = "div.artical-content"
			sel2 = soup2.select(str02)
			text01 = soup2.select("h1.artical-title")[0].text
			text02 = []
			text04 = ""
			for p in sel2[0].find_all('p'):
				text02.append(p.text)
			for p in soup2.select("span.hash-tag"):
				text04+=(p.text)	
			text03 = soup2.select("p.artical-time")[0].text
			md.update((str)(text01+text03+text_club).encode('utf-8'))                   #制定需要加密的字符串
			news_dict['id'] = md.hexdigest()
			news_dict['title'] = text01
			news_dict['content'] = text02
			news_dict['category'] = u
			date = datetime.datetime.strptime(text03, "%Y/%m/%d %H:%M")
			news_dict['date'] = date
			news_dict['news_club'] = text_club
			news_dict['tag'] = text04
			news_dict['url'] = gurl

			# print(news_dict)
			# print("\naaaaaaaaaaaaaaaaaaaaaaaa\n\n")

			mongodb.logindb();
			x = collection.update_many({"id": news_dict['id']}, {"$set": news_dict}, upsert=True)
except Exception as e:
	print("cts")
	print(e)
		