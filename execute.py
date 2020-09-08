import datetime
import time
import pymysql
import os
def doSth():


    os.system('python3 cts_crawler.py')
    os.system('python3 chinatimes_bug_new.py')
    os.system('python3 udn_crawler.py')
    os.system('python3 tvbs_crawler.py')
    os.system('python3 ltn_crawler.py')
    os.system('python3 storm_crawler.py')
    os.system('python3 nownews_crawler.py')
    os.system('python3 ettoday_crawler.py')
    os.system('python3 cna_crawler.py')
    os.system('python3 factcheckcenter_crawler.py')
    os.system('python3 rumtoast_crawler.py')
    os.system('python3 ebc_crawler.py')
    time.sleep(60)

def main(m=20):

    '''h表示設定的小時，m為設定的分鐘'''

    while True:

        # 判斷是否達到設定時間，例如23:00

        while True:

            now = datetime.datetime.now()

            # 到達設定時間，結束內迴圈

            if now.minute==m:

                break

            # 不到時間就等20秒之後再次檢測

            time.sleep(20)

        # 做正事，一天做一次
        print("hahaha")
        doSth()
if __name__ == '__main__':
    main()