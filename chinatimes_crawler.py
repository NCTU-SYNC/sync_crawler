# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash,db_init,db_update
import time
import hashlib

media = '中時'

#db initialization
collection = db_init(media)

#retrieve news list for first five pages
links = ['https://www.chinatimes.com/realtimenews/','https://www.chinatimes.com/realtimenews/?page=2',
        'https://www.chinatimes.com/realtimenews/?page=3','https://www.chinatimes.com/realtimenews/?page=4',
        'https://www.chinatimes.com/realtimenews/?page=5']
urls = []
for link in links:
    soup = get_page(link)
    sel = soup.find_all('div', class_='articlebox-compact')

    for s in sel:
        u = s.find(class_='title').find('a')['href']
        urls.append('https://chinatimes.com'+u)

news_count = 0
for url in urls:
    try:
        soup = get_page(url)
        
        title = soup.find(class_='article-title').text
        datetime = soup.find('time') #time
        modified_date = datetime.find(class_='hour').text + ' ' + datetime.find(class_='date').text #full date
        category = soup.find_all(class_='breadcrumb-item')[1].text.strip()
        tags_span = soup.find_all(class_='hash-tag')
        tags = []
        for tag in tags_span:
            cur_tag = tag.text.strip()
            cur_tag = cur_tag[1:]
            tags.append(cur_tag)

        content = []
        content_str = ""
        content_str += title
        article_body = soup.find(class_='article-body').find_all('p')
        for p in article_body:
            part = p.text
            #skip if empty
            if not part:
                continue
            content.append(part)
            content_str += part

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
        news_count+=1
        
    except Exception as e:
        print('chinatimes')
        print(e)
        continue
