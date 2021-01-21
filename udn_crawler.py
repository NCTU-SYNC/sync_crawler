# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup as bs4
import time
import codecs
import hashlib


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
news_dict = {}

media = '聯合'
md = hashlib.md5()

#retrieve news list
main_link = 'https://udn.com/news/breaknews/1/99#breaknews'
r = requests.get(main_link,headers=headers)
r.encoding='UTF-8'
soup = bs4(r.text,'html.parser')
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
        #for particular soup
        r_each = requests.get(url_each,headers=headers)
        r_each.encoding = 'UTF-8'
        soup_each = bs4(r_each.text,'html.parser')
        
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
