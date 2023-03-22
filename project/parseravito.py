import requests
from bs4 import BeautifulSoup
import lxml

import collections.abc
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping

from hyper.contrib import HTTP20Adapter

s = requests.Session()
s.mount('https://',  HTTP20Adapter())
url = 'https://www.avito.ru/zelenodolsk/kvartiry/prodam-ASgBAgICAUSSA8YQ'
response = s.get(url=url)

soup = BeautifulSoup(response.text, 'lxml')


data = soup.find('div', class_='items-items-kAJAg')


for temp in data:
    print(temp.get('id'))
    price = temp.find_all('meta',attrs = {'itemprop' : "price"})
    price_result = str(price).split('"')
    print(price_result[1])
    
    



