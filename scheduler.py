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

def store_database(media,num_of_articles):
    u.log_info('Crawling {} ...'.format(media))
    collection = u.db_init('sync_local',media)
    collection_main = u.db_init('sync',media)
    recent_news = crawlers[media](num_of_articles)
    u.log_info('Updating database ...')
    for article in recent_news:
        u.dbs_update(collection,collection_main,article)
    u.log_info('Update complete.')

# delete database portion
def delete_n_articles(media,n):
    """ Delete oldest n articles of the collection """
    collection = u.db_init('sync_local',media)
    oldest_n = list(collection.find().sort('modified_date',pymongo.ASCENDING).limit(n))
    for document in oldest_n:
        doc_id = document['_id']
        collection.delete_one({'_id':doc_id})

#Jobs
def chinatimes(num_of_articles):
    store_database('chinatimes',num_of_articles)

def cna(num_of_articles):
    store_database('cna',num_of_articles)

def cts(num_of_articles):
    store_database('cts',num_of_articles)

def ebc(num_of_articles):
    store_database('ebc',num_of_articles)

def ettoday(num_of_articles):
    store_database('ettoday',num_of_articles)

def factcheckcenter(num_of_articles):
    store_database('factcheckcenter',num_of_articles)

def ltn(num_of_articles):
    store_database('ltn',num_of_articles)

def storm(num_of_articles):
    store_database('storm',num_of_articles)

def udn(num_of_articles):
    store_database('udn',num_of_articles)
    
def clear_databases(n):
    u.log_info('Local database size check...')
    for media in crawlers:
        collection = u.db_init('sync_local',media)
        u.log_info('Checking: {} ...'.format(media))
        collection_size = collection.estimated_document_count()
        if collection_size > 40:
            u.log_info('{0} has {1} documents. Begin deletion ...'.format(media,collection_size))
            delete_n_articles(media,n)

schedule.every(CHINATIMES_FREQ).minutes.do(chinatimes,num_of_articles=CHINATIMES_NUM)
schedule.every(CNA_FREQ).minutes.do(cna,num_of_articles=CNA_NUM)
schedule.every(CTS_FREQ).minutes.do(cts,num_of_articles=CTS_NUM)
schedule.every(EBC_FREQ).minutes.do(ebc,num_of_articles=EBC_NUM)
schedule.every(ETTODAY_FREQ).minutes.do(ettoday,num_of_articles=ETTODAY_NUM)
schedule.every(FACTCHECKCENTER_FREQ).minutes.do(factcheckcenter,num_of_articles=FACTCHECKCENTER_NUM)
schedule.every(LTN_FREQ).minutes.do(ltn,num_of_articles=LTN_NUM)
schedule.every(STORM_FREQ).minutes.do(storm,num_of_articles=STORM_NUM)
schedule.every(UDN_FREQ).minutes.do(udn,num_of_articles=UDN_NUM)
schedule.every(20).minutes.do(clear_databases,30)

while True:
    schedule.run_pending()
    time.sleep(1)
