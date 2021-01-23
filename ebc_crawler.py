# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page
import time
import hashlib


url_base = "https://news.ebc.net.tw/"
urls = []
news_dict = {}

media = "東森"
md = hashlib.md5()
soup = get_page("https://news.ebc.net.tw/realtime")
sel = soup.find('div', 'news-list-box').find_all('div', 'style1 white-box') #get news list

for s in sel:
	urls.append(url_base + s.find('a')['href'])
	

count = 0		
for url in urls:
	soup = get_page(url)
	try:
		category = soup.find('div', id = 'web-map').find_all('a')[1].text
		title = soup.find('div', 'fncnews-content').find('h1').text

		content_sel = soup.find('div', 'raw-style').find_all('p')
		article_content = []
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
		date = gray_text[0]+' '+gray_text[1]

		news_dict['id'] = count
		news_dict['title'] = title
		news_dict['content'] = article_content
		news_dict['category'] = category
		news_dict['pubdate'] = date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url
		print(news_dict)

		count += 1

	except Exception as e:
		print("東森ebc")
		print(url)
		print(e)
		continue