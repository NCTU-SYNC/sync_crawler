# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash
import utilities
import time,datetime
import hashlib

def ebc_crawler(size=30):
	
	media = '東森'
	article_list = list()

	urls = []
	links = ['https://news.ebc.net.tw/realtime','https://news.ebc.net.tw/realtime?page=2',
			'https://news.ebc.net.tw/realtime?page=3','https://news.ebc.net.tw/realtime?page=4']
		
	for link in links:
		soup = get_page(link)
		sel = soup.find('div', 'news-list-box').find_all('div', 'style1 white-box') #get news list

		url_base = "https://news.ebc.net.tw"
		for s in sel:
			urls.append(url_base + s.find('a')['href'])

	article_count = 0

	for url in urls:
		soup = get_page(url)
		try:
			category = soup.find('div', id = 'web-map').find_all('a')[1].text
			title = soup.find('div', 'fncnews-content').find('h1').text

			content_sel = soup.find('div', 'raw-style').find_all('p')
			article_content = []
			content_str = ""
			content_str += title
			for p in content_sel:
				content = p.text
				#clear unwanted content
				if content.startswith('★') or not content or '延伸閱讀' in content:
					continue
				if '\u3000' in content:
					content.replace('\u3000',' ')
				if '\xa0' == content:
					continue			
				article_content.append(content.strip())
				content_str += content.strip()
			
			tags = []
			try:
				sel = soup.find('div', 'keyword').find_all('a')
				for s in sel:
					tags.append(s.text)
			except:
				tags = []

			#date
			gray_text = soup.find('span', 'small-gray-text').text
			gray_text = gray_text.split()
			modified_date = gray_text[0]+' '+gray_text[1]
			modified_date = datetime.datetime.strptime(modified_date, "%Y/%m/%d %H:%M")
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

			article_count += 1
			if article_count >= size:
				break
			
		except Exception as e:
			print("東森ebc")
			print(url)
			print(e)
			continue
	
	return article_list