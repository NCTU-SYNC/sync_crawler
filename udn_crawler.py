# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page
import time
import codecs
import hashlib

news_dict = {}

media = '聯合'
md = hashlib.md5()

#retrieve news list
main_link = 'https://udn.com/news/breaknews/1/99#breaknews'
soup = get_page(main_link)
sel = soup.find_all('div', class_='story-list__text')
urls = []
for s in sel:
    u = s.find('a')['href']
    if u == '#':
        continue
    markspot = u.find('?')
    u = u[:markspot]
    urls.append(u)

news_dict = {}
count = 0
#for each individual article
for u in urls:
    try:
        url_each = 'https://udn.com/'
        url_each += u
        soup_each = get_page(url_each)
        
        title = soup_each.find(class_='article-content__title').text
        date = soup_each.find(class_='article-content__time').text
        category = soup_each.find_all(class_='breadcrumb-items')[1].text
        tags = []

        content = []
        article_body = soup_each.find(class_='article-content__editor').find_all('p')
        for p in article_body:
            content.append(p.text)

        news_dict['id'] = count
        news_dict['title'] = title
        news_dict['content'] = content
        news_dict['category'] = category
        news_dict['pubdate'] = date
        news_dict['media'] = media
        news_dict['tags'] = tags
        news_dict['url'] = url_each
        print(news_dict)
        count+=1
        
    except Exception as e:
        print('udn')
        print(e)
        print(url_each)
        continue
