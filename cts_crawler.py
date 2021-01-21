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
import datetime



#url = { '即時' : 'https://news.cts.com.tw/real/index.html', '氣象': 'https://news.cts.com.tw/weather/index.html', '反送中': 'https://news.cts.com.tw/politics/index.html', '藝文': 'https://news.cts.com.tw/arts/index.html', '娛樂': 'https://news.cts.com.tw/entertain/index.html', '運動': 'https://news.cts.com.tw/sports/index.html', '生活': 'https://news.cts.com.tw/life/index.html', '財經': 'https://news.cts.com.tw/money/index.html', '台語': 'https://news.cts.com.tw/taiwanese/index.html', '地方': 'https://news.cts.com.tw/local/index.html', '校園': 'https://news.cts.com.tw/campus/index.html', '綜合': 'https://news.cts.com.tw/general/index.html', '國際': 'https://news.cts.com.tw/international/index.html', '社會': 'https://news.cts.com.tw/society/index.html'}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

news_dict = {}

article_count = 0
url = 'https://news.cts.com.tw/real/index.html'
media = "華視"

try:
	r = requests.get(url, headers = headers)#get HTML
	r.encoding='UTF-8'
	soup = BeautifulSoup(r.text,"html.parser") 
	newslist_str = "div.newslist-container"
	list_container = soup.select(newslist_str)
	
	for a_tag in list_container[0].find_all('a', href=True):
		article_url = a_tag['href']
		n = requests.get(article_url, headers = headers)#get HTML
		n.encoding='UTF-8'
		each_soup = BeautifulSoup(n.text,"html.parser")
		content_str = "div.artical-content"
		content_sel = each_soup.select(content_str)
		title = each_soup.select("h1.artical-title")[0].text
		category = each_soup.select('div.item.menu-active')[-1].text
		article_content = []
		tags = []
		for p in content_sel[0].find_all('p'):
			article_content.append(p.text)
		
		for p in each_soup.select("span.hash-tag"):
			tags+=(p.text)

		date_text = each_soup.select("p.artical-time")[0].text
		date = datetime.datetime.strptime(date_text, "%Y/%m/%d %H:%M")
		
		news_dict['id'] = article_count
		news_dict['title'] = title
		news_dict['content'] = article_content
		news_dict['category'] = category
		news_dict['pubdate'] = date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = article_url

		print(news_dict)

		article_count+=1
		if article_count == 50:
			break

except Exception as e:
	print("cts")
	print(e)
		