# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from utilities import get_page,generate_hash
import time,datetime
import hashlib,utilities
import requests

def udn_crawler(size=30):

    media = '聯合'
    article_list = list()
    urls = list()
    pages = [1,2,3]
    try:
        for i in pages:
            response = requests.get(
                "https://udn.com/api/more",
                params={
                    'page': i,
                    'id': '',
                    'channelId': 1,
                    'cate_id': 99,
                    'type': 'breaknews'
                })
            
            json_response = response.json()
            lists = json_response['lists']
            urls.extend([ 'https://udn.com' + item['titleLink'] for item in lists ])
    
    except Exception as error:
        utilities.log_info("URL list request error.")
        print(error)

    article_count = 0
    #for each individual article
    for url in urls:
        try:
            soup = get_page(url)
            
            title = soup.find(class_='article-content__title').text
            modified_date = soup.find(class_='article-content__time').text
            modified_date = datetime.datetime.strptime(modified_date, "%Y-%m-%d %H:%M")
            modified_date = utilities.convert_to_utc(modified_date)
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

            #print(news_dict)
            article_count+=1
            
            article_list.append(news_dict)

            if article_count >= size:
                break
            time.sleep(0.5) #to prevent request error
            
        except Exception as e:
            print('udn')
            print(e)
            print(url)
            continue
    
    return article_list

if __name__ == "__main__":
    print(udn_crawler())