# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash
import utilities
import time
import hashlib
import datetime

def cts_crawler(size=30):

	media = "華視"
	article_list = list()

	urls =[]

	try:
		soup = get_page('https://news.cts.com.tw/real/index.html')
		newslist_str = "div.newslist-container"
		list_container = soup.select(newslist_str)
		a_list = list_container[0].find_all('a', href=True)
		for a_tag in a_list:
			urls.append(a_tag['href'])

	except Exception as e:
		print("cts")
		print("url list fetch error")
		print(e)

	try:
		article_count = 0
		for url in urls:
			soup = get_page(url)
			content_sel = soup.select("div.artical-content")
			title = soup.select("h1.artical-title")[0].text
			category = soup.select('div.item.menu-active')[-1].text
			article_content = []
			content_str = ""
			content_str += title
			tags = []

			for p in content_sel[0].find_all(['p','h3']):
				article_content.append(p.text)
				content_str += p.text
			
			for a in soup.select("div.news-tag")[0].find_all('a'):
				tags.append(a.text)
			
			date_text = soup.select("time.artical-time")[0].text
			modified_date = datetime.datetime.strptime(date_text, "%Y/%m/%d %H:%M")
			modified_date = utilities.convert_to_utc(modified_date)
			
			url_hash = generate_hash(url)
			content_hash = generate_hash(content_str)

			news_dict = {}

			news_dict['title'] = title
			news_dict['content'] = article_content
			news_dict['category'] = category
			news_dict['modified_date'] = modified_date
			news_dict['media'] = media
			news_dict['tags'] = tags
			news_dict['url'] = url
			news_dict['url_hash'] = url_hash
			news_dict['content_hash'] = content_hash

			#print(news_dict)
			article_list.append(news_dict)

			article_count+=1
			if article_count >= size:
				break
			
	except Exception as e:
		print("cts")
		print(url)
		print(e)
	
	return article_list