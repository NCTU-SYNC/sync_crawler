# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page
import time
import hashlib

base = "https://www.ettoday.net/"
news_dict = {}

media = "ettoday"
md = hashlib.md5()

soup = get_page("https://www.ettoday.net/news/news-list.htm")
sel = soup.find('div', 'part_list_2').find_all('h3')
count = 0

for s in sel:
	date = s.find('span').text	
	category = s.find('em').text
	url = base + s.find('a')['href']
	try:
		soup = get_page(url)
		title = soup.find('h1', 'title').text
		#print(title,u)
		content = []
		tags = []
		for p in soup.find('div','story').find_all('p'):
			pText = p.text
			
			if '►' in pText or '▲' in pText or '·' in pText or pText == '' or '▼' in pText:
				continue
			if '更多鏡週刊報導' in pText or '你可能也想看' in pText or '其他新聞' in pText or '其他人也看了' in pText or '更多新聞' in pText:
				break
			
			content.append(p.text)
		#find tags
		tags = soup.find("meta",attrs={"name": "news_keywords"}).attrs['content'].split(',')
		#print(test[])
		news_dict['id'] = count
		news_dict['title'] = title
		news_dict['content'] = content
		news_dict['category'] = category
		news_dict['pubdate'] = date
		news_dict['media'] = media
		news_dict['tags'] = tags
		news_dict['url'] = url
		
		print(news_dict)

		count+=1
		if count >= 50:
			break

	except Exception as e:
		print("ETtoday")
		print(url)
		print(e)
		continue
