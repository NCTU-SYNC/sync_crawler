# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utilities import get_page,generate_hash
import utilities
import time,datetime
import hashlib

def ettoday_crawler(size=30):

	base = "https://www.ettoday.net"

	media = 'ettoday'
	article_list = list()

	#initiate chrome webdriver

	options = Options()
	options.add_argument("--disable-notifications")
	options.headless = True

	driver = webdriver.Chrome('chromedriver', options=options)
	driver.get("https://www.ettoday.net/news/news-list.htm")
	for _ in range(1,3):
		driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
		time.sleep(3)

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	sel = soup.find('div', 'part_list_2').find_all('h3')
	article_count = 0

	#exit selenium
	driver.quit()

	for s in sel:
		modified_date = s.find('span').text
		modified_date = datetime.datetime.strptime(modified_date, "%Y/%m/%d %H:%M")
		modified_date = utilities.convert_to_utc(modified_date)

		category = s.find('em').text
		url = base + s.find('a')['href']
		try:
			soup = get_page(url)
			title = soup.find('h1', 'title').text

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

			#print(news_dict)
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