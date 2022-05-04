# -!- coding: utf-8 -!-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utilities import get_page,generate_hash
import time,datetime
import hashlib,utilities

def udn_crawler(size=30):

    media = '聯合'
    article_list = list()

    try:
        #initiate chrome webdriver
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--window-size=1920,1080")
        options.headless = True
        driver = webdriver.Chrome('chromedriver', options=options)
        driver.get("https://udn.com/news/breaknews/1/99#breaknews")

        for _ in range(1,5):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
    
    except Exception as error:
        utilities.log_info("Selenium start error, error code:")
        print(error)
        driver.quit()
        soup = get_page("https://udn.com/news/breaknews/1/99#breaknews")
    
    sel = soup.find_all('div', class_='story-list__text')

    urls = []
    for s in sel:
        try:
            u = s.find('a')['href']
        except Exception as error:
            print(error)
            print(s)
            continue
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
