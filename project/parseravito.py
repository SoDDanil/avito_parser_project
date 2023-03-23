import requests
from bs4 import BeautifulSoup
import lxml

import pandas as pd

import collections.abc
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping

from hyper.contrib import HTTP20Adapter

s = requests.Session()
s.mount('https://',  HTTP20Adapter())
url = 'https://www.avito.ru/zelenodolsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?p=1'
response = s.get(url=url)

print(response.status_code)
soup = BeautifulSoup(response.text, 'lxml')


data = soup.find('div', class_='items-items-kAJAg')
countPages = soup.find_all('span',class_='pagination-item-JJq_j')[-2].text

arrPrice = []
arrId = []
arrHref = []

for temp in data:
    
    href = temp.get('href')
    arrHref.append(href)
    arrId.append( temp.get('id'))
    price = temp.find_all('meta',attrs = {'itemprop' : "price"})
    arrPrice.append(price)
    try:
        price_result = str(price).split('"')
    except:
        print("Неполучилось ") 

""" for pageNumber in range(2,int(countPages)+1):
    url = f'https://www.avito.ru/zelenodolsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?p={pageNumber}'
    response = s.get(url=url)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find('div', class_='items-items-kAJAg')
    for temp in data:
        arrId.append( temp.get('id'))
        price = temp.find_all('meta',attrs = {'itemprop' : "price"})
        arrPrice.append(price)
        try:
            price_result = str(price).split('"')
        except:
            print("Неполучилось ") """

df = pd.DataFrame({'Цена' : arrPrice,
                   'id' : arrId
                   })

df.to_excel('data.xlsx',index=False)