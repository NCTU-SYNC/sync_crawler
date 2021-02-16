# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash
import time,datetime
import utilities
import hashlib

def storm_crawler(size=30):

	urls = []
	media = "風傳媒"
	article_list = list()


	links = ["https://www.storm.mg/articles","https://www.storm.mg/articles/2",
			"https://www.storm.mg/articles/3","https://www.storm.mg/articles/4",
			"https://www.storm.mg/articles/5","https://www.storm.mg/articles/6"]

	for link in links:
		soup = get_page(link)
		sel = soup.find_all('div', 'category_card card_thumbs_left')

		for s in sel:
			urls.append(s.find('a')['href'])

	article_count = 0
	for url in urls:
		category = []
		try:
			soup = get_page(url)
			sel = soup.find('div', id = 'title_tags_wrapper')
			for s in sel.find_all('a'):
				category.append(s.get_text())
			title = soup.find('h1', id = 'article_title').text	
			content = []
			content_str = ""
			content_str += title
			tags = []
			for p in soup.find('div', id = 'CMS_wrapper').find_all('p'):
				content.append(p.text)
				content_str += p.text
			modified_date = soup.find('span', id = 'info_time').text
			modified_date = datetime.datetime.strptime(modified_date, "%Y-%m-%d %H:%M")
			modified_date = utilities.convert_to_utc(modified_date)
			
			url_hash = generate_hash(url)
			content_hash = generate_hash(content_str)

			news_dict = {}
			news_dict['title'] = title
			news_dict['content'] = content
			news_dict['category'] = category
			news_dict['modified_date'] = modified_date
			news_dict['media'] = media
			news_dict['tags'] = tags
			news_dict['url'] = url
			news_dict['url_hash'] = url_hash
			news_dict['content_hash'] = content_hash

			article_list.append(news_dict)
			#print(news_dict)
			article_count+=1
			
			if article_count >= size:
				break
			
		except Exception as e:
			print("風傳媒storm")
			print(url)
			print(e)
			continue
	
	return article_list