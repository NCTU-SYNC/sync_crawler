# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page
import time
import codecs
import hashlib

news_dict = {}
media = '中時'
md = hashlib.md5() #for hash

#retrieve news list for first two pages
links = ['https://www.chinatimes.com/realtimenews/','https://www.chinatimes.com/realtimenews/?page=2']
urls = []
for link in links:
    soup = get_page(link)
    sel = soup.find_all('div', class_='articlebox-compact')

    for s in sel:
        #NOT FULL URL
        u = s.find(class_='title').find('a')['href']
        urls.append(u)

article_count = 0
for u in urls:
    try:
        #create full url
        url_each = 'https://chinatimes.com'
        url_each+=u
        
        #for particular soup
        soup_each = get_page(url_each)
        
        title = soup_each.find(class_='article-title').text
        datetime = soup_each.find('time') #time
        date = datetime.find(class_='hour').text + ' ' + datetime.find(class_='date').text #full date
        category = soup_each.find_all(class_='breadcrumb-item')[1].text.strip()
        tags_span = soup_each.find_all(class_='hash-tag')
        tags = []
        for tag in tags_span:
            cur_tag = tag.text.strip()
            cur_tag = cur_tag[1:]
            tags.append(cur_tag)

        content = []

        article_body = soup_each.find(class_='article-body').find_all('p')
        for p in article_body:
            part = p.text
            #skip if empty
            if not part:
                continue
            content.append(part)

        news_dict['id'] = article_count
        news_dict['title'] = title
        news_dict['content'] = content
        news_dict['category'] = category
        news_dict['pubdate'] = date
        news_dict['media'] = media
        news_dict['tags'] = tags
        news_dict['url'] = url_each
        article_count+=1
        print(news_dict)

    except Exception as e:
        print('chinatimes')
        print(e)
        continue
