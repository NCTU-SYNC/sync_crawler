# -!- coding: utf-8 -!-
from utilities import get_page,generate_hash
import utilities
import datetime

def chinatimes_crawler(size=30):

    media = '中時'
    article_list = []

    # get news list for first five pages
    newslist_page = ['https://www.chinatimes.com/realtimenews/','https://www.chinatimes.com/realtimenews/?page=2',
            'https://www.chinatimes.com/realtimenews/?page=3','https://www.chinatimes.com/realtimenews/?page=4',
            'https://www.chinatimes.com/realtimenews/?page=5']
    urls = []
    for page in newslist_page:
        try:
            soup = get_page(page)
            sel = soup.find_all('div', class_='articlebox-compact')

            for s in sel:
                u = s.find(class_='title').find('a')['href']
                urls.append('https://www.chinatimes.com'+u)
        except Exception as error:
            print("Get article url link error.")
            print(page)

    news_count = 0
    for url in urls:
        try:

            soup = get_page(url)
            
            title = soup.find(class_='article-title').text
            date_tag = soup.find('time') #time
            modified_date = date_tag.find(class_='hour').text + ' ' + date_tag.find(class_='date').text #full date
            modified_date = datetime.datetime.strptime(modified_date, "%H:%M %Y/%m/%d")
            modified_date = utilities.convert_to_utc(modified_date)
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

            #print(news_dict)
            article_list.append(news_dict)

            news_count+=1

            if news_count >= size:
                break
            
        except Exception as e:
            print('chinatimes')
            print(url)
            print(e)
            continue
    
    return article_list