# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page
import time
import codecs
import hashlib

news_dict = {}

media = "中央社"

soup = get_page("https://www.cna.com.tw/list/aall.aspx")
sel = soup.find('ul', 'mainList imgModule', id = 'jsMainList').find_all('li')

#add each url to url list
urls = []
for s in sel:
	urls.append(s.find('a')['href'])

newscount = 0
for url in urls:
	soup = get_page(url)
	try:
		category = soup.find('div', 'breadcrumb').find_all('a')[1].text
		title = soup.find('div', 'centralContent').find('h1').text
		sel = soup.find('div', 'paragraph').find_all('p')
		article_content = []
		tags = []
		for s in sel:
			article_content.append(s.text)

		date = soup.find('div', 'updatetime').find('span').text
		
		news_dict['id'] = newscount #hash -> need to change
		news_dict['title'] = title
		news_dict['content'] = article_content
		news_dict['category'] = category
		news_dict['pubdate'] = date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url
		newscount+=1
		
		print(news_dict) #insert to db, currently print
		
	except Exception as e:
		print("中央社cna")
		print(url)
		print(e)
		continue