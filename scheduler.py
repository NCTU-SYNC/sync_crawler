from chinatimes_crawler import chinatimes_crawler
from cna_crawler import cna_crawler
from cts_crawler import cts_crawler
from ebc_crawler import ebc_crawler
from ettoday_crawler import ettoday_crawler
from factcheckcenter_crawler import factcheckcenter_crawler
from ltn_crawler import ltn_crawler
from storm_crawler import storm_crawler
from udn_crawler import udn_crawler
from pymongo import MongoClient
import utilities as u
import schedule,time,pymongo

MONGODB_URI_LOCAL = 'mongodb://localhost:27017/'
MONGODB_URI_MAIN  = '' #put in sync main database uri
LOCAL_DATABASE = 'test_sync_local'
LOCAL_COLLECTION = 'news'
MAIN_DATABASE = 'sync'
MAIN_COLLECTION = 'test_news'

CHINATIMES_FREQ = 10
CNA_FREQ = 10
CTS_FREQ = 10
EBC_FREQ = 10
ETTODAY_FREQ = 10
FACTCHECKCENTER_FREQ = 10
LTN_FREQ = 10
STORM_FREQ = 10
UDN_FREQ = 10

CHINATIMES_NUM = 30
CNA_NUM = 30
CTS_NUM = 30
EBC_NUM = 30
ETTODAY_NUM = 30
FACTCHECKCENTER_NUM = 30
LTN_NUM = 30
STORM_NUM = 30
UDN_NUM = 30

MEDIA_LIST = ['中時','中央社','華視','東森','ettoday','台灣事實查核中心','自由時報','風傳媒','聯合']
MEDIA_LIST_EN = ['chinatimes', 'cna', 'cts', 'ebc', 'ettoday', 'factcheckcenter', 'ltn', 'storm', 'udn']

crawlers = {
    'chinatimes'     : chinatimes_crawler,
    'cna'            : cna_crawler,
    'cts'            : cts_crawler,
    'ebc'            : ebc_crawler,
    'ettoday'        : ettoday_crawler,
    'factcheckcenter': factcheckcenter_crawler,
    'ltn'            : ltn_crawler,
    'storm'          : storm_crawler,
    'udn'            : udn_crawler
}

def crawl_and_store(media,num_of_articles,mongodb_uri_local,mongodb_uri_main):
    u.log_info('Crawling {} ...'.format(media))

    collection_local = u.get_db_instance(LOCAL_DATABASE,LOCAL_COLLECTION,mongodb_uri_local)
    collection_main = u.get_db_instance(MAIN_DATABASE,MAIN_COLLECTION,mongodb_uri_main)
    recent_news = crawlers[media](num_of_articles)
    u.log_info('Updating database ...')
    for article in recent_news:
        u.update_dbs(collection_local,collection_main,article)
    u.log_info('Update complete.')

def delete_n_documents(collection,media,n):
    """ Delete n of the oldest articles of from the collection """
    oldest_n = list(collection.find({'media':media}).sort('modified_date',pymongo.ASCENDING).limit(n))
    for document in oldest_n:
        doc_id = document['_id']
        collection.delete_one({'_id':doc_id})

#Jobs
def chinatimes(num_of_articles):
    crawl_and_store('chinatimes',num_of_articles,MONGODB_URI_LOCAL,MONGODB_URI_MAIN)

def cna(num_of_articles):
    crawl_and_store('cna',num_of_articles,MONGODB_URI_LOCAL,MONGODB_URI_MAIN)

def cts(num_of_articles):
    crawl_and_store('cts',num_of_articles,MONGODB_URI_LOCAL,MONGODB_URI_MAIN)

def ebc(num_of_articles):
    crawl_and_store('ebc',num_of_articles,MONGODB_URI_LOCAL,MONGODB_URI_MAIN)

def ettoday(num_of_articles):
    crawl_and_store('ettoday',num_of_articles,MONGODB_URI_LOCAL,MONGODB_URI_MAIN)

def factcheckcenter(num_of_articles):
    crawl_and_store('factcheckcenter',num_of_articles,MONGODB_URI_LOCAL,MONGODB_URI_MAIN)

def ltn(num_of_articles):
    crawl_and_store('ltn',num_of_articles,MONGODB_URI_LOCAL,MONGODB_URI_MAIN)

def storm(num_of_articles):
    crawl_and_store('storm',num_of_articles,MONGODB_URI_LOCAL,MONGODB_URI_MAIN)

def udn(num_of_articles):
    crawl_and_store('udn',num_of_articles,MONGODB_URI_LOCAL,MONGODB_URI_MAIN)
    
def clear_local_database(n,limit,mongodb_uri_local):
    """ Check each media, delete n documents if # of current documents exceed limit.

        Arguments:
        n    : number of documents to delete
        limit: start deletion if number of documents of each media exceeds limit
    """
    u.log_info('Local database size check...')
    for media in MEDIA_LIST:
        collection = u.get_db_instance(LOCAL_DATABASE,LOCAL_COLLECTION,mongodb_uri_local)
        #u.log_info('Checking: {} ...'.format(media))
        current_size = collection.count_documents({'media':media})
        if current_size > limit:
            u.log_info('{0} has {1} documents. Begin deletion ...'.format(media,current_size))
            delete_n_documents(collection,media,n)
            current_count = collection.count_documents({'media':media})
            u.log_info('count after deletion:{}'.format(current_count))


schedule.every(CHINATIMES_FREQ).minutes.do(chinatimes,num_of_articles=CHINATIMES_NUM)
schedule.every(CNA_FREQ).minutes.do(cna,num_of_articles=CNA_NUM)
schedule.every(CTS_FREQ).minutes.do(cts,num_of_articles=CTS_NUM)
schedule.every(EBC_FREQ).minutes.do(ebc,num_of_articles=EBC_NUM)
schedule.every(ETTODAY_FREQ).minutes.do(ettoday,num_of_articles=ETTODAY_NUM)
schedule.every(FACTCHECKCENTER_FREQ).minutes.do(factcheckcenter,num_of_articles=FACTCHECKCENTER_NUM)
schedule.every(LTN_FREQ).minutes.do(ltn,num_of_articles=LTN_NUM)
schedule.every(STORM_FREQ).minutes.do(storm,num_of_articles=STORM_NUM)
schedule.every(UDN_FREQ).minutes.do(udn,num_of_articles=UDN_NUM)
schedule.every(20).minutes.do(clear_local_database,n=30,limit=40,mongodb_uri_local=MONGODB_URI_LOCAL)

while True:
    schedule.run_pending()
    time.sleep(1)
