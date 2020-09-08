import requests
import csv
from bs4 import BeautifulSoup
import time
import codecs
from os import listdir
from os.path import isfile, isdir, join
# encoding:utf-8
import json
#from firebase import firebase
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# from firebase import firebase
import mongodb
from mongodb import collection

import hashlib

# key="YNkwUyNwermCmVVgovfdSiyYcjYLh2oNKaHOx452"

# authentication = firebase.FirebaseAuthentication(key, 'muilabatnctu@gmail.com')

# firebase.authentication = authentication

# user = authentication.get_user()

# firebase = firebase.FirebaseApplication('https://sync-7f2a5.firebaseio.com/', authentication=authentication)


filename = "中時電子報2.csv"
# timename += time.strftime("%Y-%m-%d-(%H)", time.localtime(time.time()))
# timename+=".csv"
url = { '政治' : 'https://www.chinatimes.com/politic/total/?chdtv', '言論': 'https://www.chinatimes.com/opinion/total/?chdtv', '生活': 'https://www.chinatimes.com/life/total/?chdtv', '娛樂': 'https://www.chinatimes.com/star/total/?chdtv', '財經': 'https://www.chinatimes.com/money/realtimenews/?chdtv', '社會': 'https://www.chinatimes.com/society/total/?chdtv', '話題': 'https://www.chinatimes.com/hottopic/total/?chdtv', '國際': 'https://www.chinatimes.com/world/total/?chdtv', '軍事': 'https://www.chinatimes.com/armament/total/?chdtv', '兩岸': 'https://www.chinatimes.com/chinese/total/?chdtv', '時尚': 'https://www.chinatimes.com/fashion/total/?chdtv', '體育': 'https://www.chinatimes.com/sports/total/?chdtv', '科技': 'https://www.chinatimes.com/technologynews/total/?chdtv', '旅遊': 'https://www.chinatimes.com/travel/total/?chdtv'}
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


# with codecs.open(timename, "r+", encoding = 'utf_8_sig') as csvFile:

#   # 讀取 CSV 檔案內容
#   rows = csv.reader(csvFile)

#   # 以迴圈輸出每一列
#   for row in rows:
#     print(row[1])
news_dict = {}
# with codecs.open(timename, "r+", encoding = 'utf_8_sig') as csvFile:

#   # 讀取 CSV 檔案內容
count = 0
#   # 以迴圈輸出每一列
# 	# for row in rows:
# 	# 	print(row[1])
# 	# count = int(len(csvFile.readlines()))-1
# 	# print(count)
# 	#定義欄位
# 	fieldNames = ['id', '標題', '內文']

# 	#將dictionary寫入CSV檔
# 	writer = csv.DictWriter(csvFile, fieldNames)

	# 寫入第一列的欄位名稱
	# writer.writeheader()
countflag = 0
text_club = "中時"
md = hashlib.md5()
try:
	for u in  url:
		r = requests.get(url[u], headers = headers)#get HTML
		soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
		str01 = "div.cropper"
		sel = soup.select(str01)
		i = 0
		for s in sel:
			flag = 0
			#duplicate = 0
			gurl = "https://www.chinatimes.com"
			gurl += sel[i].find('a')['href']
			n = requests.get(gurl, headers = headers)#get HTML
			soup2 = BeautifulSoup(n.text,"html.parser") #將網頁資料以html.parser
			str02 = "div.article-body"
			sel2 = soup2.select(str02)
			text01 = soup2.select("h1.article-title")[0].text
			text02 = ""
			text04 = ""
			for p in sel2[0].find_all('p'):
				text02+=(p.text)
			for p in soup2.select("span.hash-tag"):
				text04+=(p.text+",")	
			i+=1
			text03 = soup2.find("time")['datetime']
			md.update((str)(text01+text03+text_club).encode('utf-8'))                   #制定需要加密的字符串
			news_dict['id'] = md.hexdigest()
			news_dict['title'] = text01
			news_dict['content'] = text02
			news_dict['category'] = u
			news_dict['date'] = text03
			news_dict['news_club'] = text_club
			news_dict['tag'] = text04
			news_dict['url'] = gurl
			#news_fb = firebase.get("/news", None)
			# for key,value in news_fb.items():
			# 	if(news_dict['標題']==format(value["標題"])):
			# 		duplicate = 1
			# 	if countflag==0:
			# 		count+=1
			# countflag = 1		
			# if duplicate==0:
			# 	js = json.dumps(news_dict, sort_keys=True, indent=4, separators=(',', ':'),ensure_ascii=False)
			# 	count+=1
			# 	news_dict['id'] = str(count)
			# 	firebase.post("/news", news_dict)		
			
			# firebase.put("/news/"+news_dict['id'], '標題', news_dict['標題'])
			# firebase.put("/news/"+news_dict['id'], '內文', news_dict['內文'])
			# firebase.put("/news/"+news_dict['id'], '分類', news_dict['分類'])
			# firebase.put("/news/"+news_dict['id'], '新聞時間', news_dict['新聞時間'])
			# firebase.put("/news/"+news_dict['id'], '新聞社', news_dict['新聞社'])
			# print(news_dict)
			# print("\naaaaaaaaaaaaaaaaaaaaaaaa\n\n")

			mongodb.logindb();
			x = collection.update_many({"id": news_dict['id']}, {"$set": news_dict}, upsert=True)
except Exception as e:
	print("中時chinatimes")
	print(e)

# with codecs.open(timename, "r+", encoding = 'utf_8_sig') as csvFile:
# 	rows = csv.reader(csvFile)
# 	for row in rows:
# 		count+=1
# 	print(count)	
#def crawler(filename, url, gurl, text):
