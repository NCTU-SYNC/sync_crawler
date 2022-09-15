# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash
import utilities
import time,datetime
import hashlib

def setn_crawler(size=30):
	
	media = '三立'

	urls = []
	view_all_link = "https://www.setn.com/ViewAll.aspx"
	base= 'https://www.setn.com'

	try:
		soup = get_page(view_all_link)
		sel = soup.find_all('h3',class_='view-li-title')
	except Exception as e:
		print("三立setn")
		print('Fetch news list error')
		print(view_all_link)
		print(e)
		return []

	urls = [ base + tag.a['href'] if tag.a['href'][0]=='/' else tag.a['href'] for tag in sel ]

	article_list = []
	article_count = 0

	for url in urls:
		try:
			soup = get_page(url)
			category = soup.find('meta',attrs={'property':'article:section'})['content']
			title = soup.find('h1').text
			content_sel = soup.find('article').find_all('p')
			article_content = [ p.text for p in content_sel if p.text != '']
			content_str = title + ''.join(article_content)
			tags = soup.find('meta', attrs={'name':'news_keywords'})['content'].split(',')

			try:
				time = soup.find('time',class_='page-date').text
				modified_date = datetime.datetime.strptime(time, "%Y/%m/%d %H:%M:%S")
			except AttributeError:
				time = soup.find(class_='newsTime').time.text
				modified_date = datetime.datetime.strptime(time, "%Y/%m/%d %H:%M")
			
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
			
			article_list.append(news_dict)
			article_count += 1
			if article_count >= size:
				break
			
		except Exception as e:
			print("三立setn")
			print(url)
			print(e)
			continue
	
	return article_list