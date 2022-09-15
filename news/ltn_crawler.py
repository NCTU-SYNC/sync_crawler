# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash
import utilities
import json
import time,datetime
import hashlib

url_title = ["https://news.ltn.com.tw/ajax/breakingnews/all/1", "https://news.ltn.com.tw/ajax/breakingnews/all/2", "https://news.ltn.com.tw/ajax/breakingnews/all/3", "https://news.ltn.com.tw/ajax/breakingnews/all/4", "https://news.ltn.com.tw/ajax/breakingnews/all/5"]
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

def get_one_page(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
        	return response.json()
        return None
    except :
        print("page fetch fail")

def parse_data(urls):
	first = True
	count = 20
	for url in url_title:
        #obtain json from ltnnews ajax
		data = get_one_page(url)
        #page1 and remaining pages are in different format, therefore different strategies applied
		if first:
            #'data' is in a form of a list of articles, for each article, obtain url
			for url in data['data']:
				urls.append(url['url'])	
		else:
			try:
				for _ in range(20):
					number = str(count)
					urls.append(data['data'][number]['url'])
					count+=1
			except TypeError as e:
				print('Parse data error!')
				print(e)				
		first = False

def ltn_crawler(size=30):

	categories = {'health':'健康', 'video':'影音', 'ec':'財經', 'ent':'娛樂', 'auto':'汽車', 'istyle':'時尚','sports':'體育', '3c':'3C科技', 'talk':'評論','playing':'玩咖','food':'食譜','estate':'地產'}
	urls = []
	try:
		parse_data(urls)
	except Exception as e:
		print("自由時報ltn")
		print('parse data error')
		print(e)
		return []
	
	media = '自由時報'
	article_list = list()

	article_count = 0
	for url in urls:
		try:
			soup = get_page(url)
			title = soup.find('h1').text
			content = []
			content_str = ""
			content_str += title
			tags = []
			
			#website has been partly rewritten, therefore have to try two possibilities
			try:
				allpara = soup.find('div', attrs={'data-desc':'內容頁'}).find_all('p')
				pcount = len(allpara)
			except AttributeError:
				allpara = soup.find('div', attrs={'data-desc':'內文'}).find_all('p')
				pcount = len(allpara)
			
			for p in allpara:
				if pcount == 1:
					break
				para = p.text
				if '請繼續往下閱讀' in para:
					continue
				content.append(p.text)
				content_str += p.text
				pcount -= 1
			
			start = url.find('//')+2
			link_cat = url[start:url.find('.')]
			if categories.get(link_cat):
				category = categories[link_cat]
			else:
				try:
					category = soup.find('div', 'breadcrumbs boxTitle boxText').text
					category = category[6:].strip()
				except AttributeError:
					print('Error when finding category.')
					raise AttributeError
			
			modified_date = soup.find('span', 'time').text.strip()[:16]
			try:
				modified_date = datetime.datetime.strptime(modified_date, "%Y/%m/%d %H:%M")
			except ValueError:
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

			article_count+=1
			if article_count >= size:
				break

		except Exception as e:
			print("自由時報ltn")
			print(url)
			print(e)
			continue
	
	return article_list