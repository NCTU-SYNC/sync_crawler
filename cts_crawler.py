# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page
import time
import hashlib
import datetime

news_dict = {}

article_count = 0
url = 'https://news.cts.com.tw/real/index.html'
media = "華視"

try:
	soup = get_page(url)
	newslist_str = "div.newslist-container"
	list_container = soup.select(newslist_str)
	a_list = list_container[0].find_all('a', href=True)

except Exception as e:
	print("cts")
	print("url list fetch error")
	print(e)

try:
	for a_tag in a_list:
		article_url = a_tag['href']
		each_soup = get_page(article_url)
		content_str = "div.artical-content"
		content_sel = each_soup.select(content_str)
		title = each_soup.select("h1.artical-title")[0].text
		category = each_soup.select('div.item.menu-active')[-1].text
		article_content = []
		tags = []
		for p in content_sel[0].find_all('p'):
			article_content.append(p.text)
		
		for a in each_soup.select("div.news-tag")[0].find_all('a'):
			tags.append(a.text)

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
	print(article_url)
	print(e)
		