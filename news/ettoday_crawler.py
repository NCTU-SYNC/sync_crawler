# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash
import utilities
import time,datetime
import hashlib
import feedparser

def ettoday_crawler(size=30):

	media = 'ettoday'
	article_list = list()

	article_count = 0
	# get newslist from rss feed
	NewsFeed = feedparser.parse("https://feeds.feedburner.com/ettoday/realtime")
	news_link_list = [ entry['link'][:-9] for entry in NewsFeed.entries ] # remove "fromrss" from link

	for url in news_link_list:
		try:
			soup = get_page(url)
			title = soup.find('h1', 'title').text
			category = soup.find(class_=['menu_bread_crumb', 'part_breadcrumb']).find_all('div')[1].text.strip()

			modified_date = soup.find('time', attrs={'itemprop': 'datePublished'})['datetime']
			modified_date = datetime.datetime.fromisoformat(modified_date)
			modified_date = utilities.convert_to_utc(modified_date)
   
			article_content = []
			content_str = ""
			content_str += title
			tags = []
			for p in soup.find('div','story').find_all('p'):
				pText = p.text
				
				if '►' in pText or '▲' in pText or '·' in pText or pText == '' or '▼' in pText:
					continue
				if '更多鏡週刊報導' in pText or '你可能也想看' in pText or '其他新聞' in pText or '其他人也看了' in pText or '更多新聞' in pText:
					break
				
				article_content.append(p.text)
				content_str += p.text
				
			#find tags
			tags = soup.find("meta",attrs={"name": "news_keywords"}).attrs['content'].split(',')

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

			article_count+=1
			if article_count >= size:
				break

		except Exception as e:
			print("ETtoday")
			print(url)
			print(e)
			continue

	return article_list