import requests
from bs4 import BeautifulSoup

headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

def get_page(url):

    """Returns a BeautifulSoup object with a given url

    Parameter type: string
    """
    r = requests.get(url, headers = headers)#get HTML
    r.encoding='UTF-8'
    soup = BeautifulSoup(r.text,"html.parser")
    return soup