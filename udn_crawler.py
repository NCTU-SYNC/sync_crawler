# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash,db_init,db_update
import time
import hashlib

media = '聯合'

#db initialization
collection = db_init(media)

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
    urls.append('https://udn.com'+u)

article_count = 0
#for each individual article
for url in urls:
    try:
        soup = get_page(url)
        
        title = soup.find(class_='article-content__title').text
        modified_date = soup.find(class_='article-content__time').text
        category = soup.find_all(class_='breadcrumb-items')[1].text
        tags = []

        content = []
        content_str = ""
        content_str += title
        article_body = soup.find(class_='article-content__editor').find_all('p')
        for p in article_body:
            p_text = p.text.strip()
            if not p_text:
                continue
            content.append(p_text)
            content_str += p_text

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

        db_update(collection,news_dict)
        print(news_dict)
        article_count+=1
        
    except Exception as e:
        print('udn')
        print(e)
        print(url)
        continue
