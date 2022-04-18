from news.chinatimes_crawler import chinatimes_crawler
from news.cna_crawler import cna_crawler
from news.cts_crawler import cts_crawler
from news.ebc_crawler import ebc_crawler
from news.ettoday_crawler import ettoday_crawler
from news.factcheckcenter_crawler import factcheckcenter_crawler
from news.ltn_crawler import ltn_crawler
from news.storm_crawler import storm_crawler
from news.udn_crawler import udn_crawler
from news.setn_crawler import setn_crawler

from pymongo import MongoClient
from configparser import ConfigParser
import utilities as u
import schedule,time,pymongo
import logging

database_config = ConfigParser(interpolation=None)
database_config.read('database_config.ini')

MONGODB_URI_LOCAL = database_config['cache']['uri']
LOCAL_DATABASE    = database_config['cache']['db']
LOCAL_COLLECTION  = database_config['cache']['collection']
MONGODB_URI_MAIN  = database_config['main']['uri']
MAIN_DATABASE     = database_config['main']['db']
MAIN_COLLECTION   = database_config['main']['collection']
DEV_MAIN_DATABASE = database_config['dev-main']['db']
DEV_MAIN_COLLECTION   = database_config['dev-main']['collection']

logging.basicConfig(filename='error_test.log' , level = logging.ERROR ,
    format = '%(asctime)s:%(levelname)s:%(message)s')

settings = ConfigParser(interpolation=None)
settings.read('crawler_settings.ini')

CHINATIMES_FREQ      = settings['freq'].getint('chinatimes')
CNA_FREQ             = settings['freq'].getint('cna')
CTS_FREQ             = settings['freq'].getint('cts')
EBC_FREQ             = settings['freq'].getint('ebc')
ETTODAY_FREQ         = settings['freq'].getint('ettoday')
FACTCHECKCENTER_FREQ = settings['freq'].getint('factcheckcenter')
LTN_FREQ             = settings['freq'].getint('ltn')
STORM_FREQ           = settings['freq'].getint('storm')
UDN_FREQ             = settings['freq'].getint('udn')
SETN_FREQ            = settings['freq'].getint('setn')

CHINATIMES_NUM      = settings['number'].getint('chinatimes')
CNA_NUM             = settings['number'].getint('cna')
CTS_NUM             = settings['number'].getint('cts')
EBC_NUM             = settings['number'].getint('ebc')
ETTODAY_NUM         = settings['number'].getint('ettoday')
FACTCHECKCENTER_NUM = settings['number'].getint('factcheckcenter')
LTN_NUM             = settings['number'].getint('ltn')
STORM_NUM           = settings['number'].getint('storm')
UDN_NUM             = settings['number'].getint('udn')
SETN_NUM            = settings['number'].getint('setn')

CLEAR_NUM   = settings['reset_cache'].getint('clear_count')
CLEAR_LIMIT = settings['reset_cache'].getint('clear_limit')
CLEAR_FREQ  = settings['reset_cache'].getint('clear_freq')

error_list=[]

MEDIA_LIST = ['中時','中央社','華視','東森','ettoday','台灣事實查核中心','自由時報','風傳媒','聯合','三立']
MEDIA_LIST_EN = ['chinatimes', 'cna', 'cts', 'ebc', 'ettoday', 'factcheckcenter', 'ltn', 'storm', 'udn', 'setn']

crawlers = {
    'chinatimes'     : chinatimes_crawler,
    'cna'            : cna_crawler,
    'cts'            : cts_crawler,
    'ebc'            : ebc_crawler,
    'ettoday'        : ettoday_crawler,
    'factcheckcenter': factcheckcenter_crawler,
    'ltn'            : ltn_crawler,
    'storm'          : storm_crawler,
    'udn'            : udn_crawler,
    'setn'           : setn_crawler
}

def crawl_and_store(media,num_of_articles):
    u.log_info('Crawling {} ...'.format(media))
    if media in error_list:
        print(f"{media} is in error list --> skip")
        return
    collection_local = u.get_db_instance(LOCAL_DATABASE,LOCAL_COLLECTION,MONGODB_URI_LOCAL)
    collection_main = u.get_db_instance(MAIN_DATABASE,MAIN_COLLECTION,MONGODB_URI_MAIN)
    print(collection_main,"....")
    collection_dev_main = u.get_db_instance(DEV_MAIN_DATABASE, DEV_MAIN_COLLECTION, MONGODB_URI_MAIN)
    try:
        recent_news = crawlers[media](num_of_articles)
    except Exception as e:
        # print(e,"...")
        error_list.append(media)
        logging.error(f"error_list: {error_list} have been stopped\n {e}")
    else:
        u.log_info('Updating database ...')
        for article in recent_news:
            u.update_dbs(collection_local,collection_main,collection_dev_main,article)
    finally:
        u.log_info('Update complete.')

def delete_n_documents(collection,media,n):
    """ Delete n of the oldest articles of from the collection """
    oldest_n = list(collection.find({'media':media}).sort('modified_date',pymongo.ASCENDING).limit(n))
    for document in oldest_n:
        doc_id = document['_id']
        collection.delete_one({'_id':doc_id})

#Jobs
def chinatimes(num_of_articles):
    crawl_and_store('chinatimes',num_of_articles)

def cna(num_of_articles):
    crawl_and_store('cna',num_of_articles)

def cts(num_of_articles):
    crawl_and_store('cts',num_of_articles)

def ebc(num_of_articles):
    crawl_and_store('ebc',num_of_articles)

def ettoday(num_of_articles):
    crawl_and_store('ettoday',num_of_articles)

def factcheckcenter(num_of_articles):
    crawl_and_store('factcheckcenter',num_of_articles)

def ltn(num_of_articles):
    crawl_and_store('ltn',num_of_articles)

def storm(num_of_articles):
    crawl_and_store('storm',num_of_articles)

def udn(num_of_articles):
    crawl_and_store('udn',num_of_articles)

def setn(num_of_articles):
    crawl_and_store('setn',num_of_articles)

def clear_local_database(n,limit):
    """ Check each media, delete n documents if # of current documents exceed limit.

        Arguments:
        n    : number of documents to delete
        limit: start deletion if number of documents of each media exceeds limit
    """
    u.log_info('Local database size check...')
    for media in MEDIA_LIST:
        collection = u.get_db_instance(LOCAL_DATABASE,LOCAL_COLLECTION,MONGODB_URI_LOCAL)
        #u.log_info('Checking: {} ...'.format(media))
        current_size = collection.count_documents({'media':media})
        if current_size > limit:
            u.log_info('{0} has {1} documents. Begin deletion ...'.format(media,current_size))
            delete_n_documents(collection,media,n)
            current_count = collection.count_documents({'media':media})
            u.log_info('count after deletion:{}'.format(current_count))


# schedule.every(CHINATIMES_FREQ).minutes.do(chinatimes,num_of_articles=CHINATIMES_NUM)
schedule.every(CNA_FREQ).minutes.do(cna,num_of_articles=CNA_NUM)
schedule.every(CTS_FREQ).minutes.do(cts,num_of_articles=CTS_NUM)
schedule.every(EBC_FREQ).minutes.do(ebc,num_of_articles=EBC_NUM)
schedule.every(ETTODAY_FREQ).minutes.do(ettoday,num_of_articles=ETTODAY_NUM)
schedule.every(FACTCHECKCENTER_FREQ).minutes.do(factcheckcenter,num_of_articles=FACTCHECKCENTER_NUM)
schedule.every(LTN_FREQ).minutes.do(ltn,num_of_articles=LTN_NUM)
schedule.every(STORM_FREQ).minutes.do(storm,num_of_articles=STORM_NUM)
schedule.every(UDN_FREQ).minutes.do(udn,num_of_articles=UDN_NUM)
schedule.every(SETN_FREQ).minutes.do(setn,num_of_articles=SETN_NUM)
schedule.every(CLEAR_FREQ).minutes.do(clear_local_database,n=CLEAR_NUM,limit=CLEAR_LIMIT)

while True:
    schedule.run_pending()
    time.sleep(1)
