import requests
from bs4 import BeautifulSoup
import lxml

from time import sleep
import pandas as pd

import collections.abc
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping

from hyper.contrib import HTTP20Adapter

class AvitoParser():

    def connection(self,url):
        s = requests.Session()
        s.mount('https://',  HTTP20Adapter())
        response = s.get(url=url)
        if response.status_code==200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        else:
            print('Неудачное соединение код ошибки',response.status_code)
            exit()
    
    def get_count_pages(self):
        url = 'https://www.avito.ru/zelenodolsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?p=1'
        soup = self.connection(url)
        return soup.find_all('span',class_='pagination-item-JJq_j')[-2].text
    
    def get_price(self,data):
        arrPrice = []
        for temp in data:
            try:
                price = temp.find_all('meta',attrs = {'itemprop' : "price"})
                priceresult = str(price).split('"')[1]
                arrPrice.append(priceresult)
            except:
                arrPrice.append('None')
        return arrPrice


    def get_adress(self,data):
        arrAdress = []
        for temp in data:
            try:
                adress = temp.find('div',attrs = {'data-marker': 'item-address'}).get_text()
                arrAdress.append(adress)
            except:
                arrAdress.append("None")
        return arrAdress
    

    def get_title(self,data):
        arrTitle = []
        for temp in data:
            try:
                title = temp.find(attrs = {'itemprop':'name'}).get_text()
                arrTitle.append(title)
            except:
                arrTitle.append("None")
        return arrTitle
        
    def get_price_meter(self,data):
        arrPriceMeter = []
        for temp in data:
            try:
                priceMeter = temp.find('span',class_='price-noaccent-X6dOy price-normalizedPrice-PplY9 text-text-LurtD text-size-s-BxGpL')
                arrPriceMeter.append(priceMeter.text)
            except:
                arrPriceMeter.append("None")
        return arrPriceMeter
    
    def get_href(self,data):
        arrHref = []
        for temp in data:
            try:
                href = 'https://www.avito.ru' + temp.find('a').get('href')
                arrHref.append(href)
            except:
                arrHref.append("None")
        return arrHref
    
    def get_id(self,data):
        arrId = []
        for temp in data:
            try:
                id = temp.get('id')
                arrId.append(id)
            except:
                arrId.append("None")
        return arrId

    def save_to_xlsx(self,arrPriceResult,arrAdressResult,arrTitleResult,arrPriceMeterResult,arrHrefResult,arrIdResult):
        df = pd.DataFrame({'Цена' : arrPriceResult,
                   'id' : arrIdResult,
                   'Ссылка' : arrHrefResult,
                   'Адрес' : arrAdressResult,
                   'Цена за метр' : arrPriceMeterResult,
                   'Титул' : arrTitleResult
                   })
        df.to_excel('data.xlsx',index=False)



    def collect_data(self):
        countPages = self.get_count_pages()
        arrPriceResult = []
        arrAdressResult = []
        arrTitleResult = []
        arrPriceMeterResult = []
        arrHrefResult = []
        arrIdResult = []
        for page in range(1,int(countPages)+1):
            sleep(10)
            print(page)
            url = f'https://www.avito.ru/zelenodolsk/kvartiry/prodam-ASgBAgICAUSSA8YQ?p={page}'
            data = self.connection(url)
            datapage = data.find('div', class_='items-items-kAJAg')
            arrPriceResult = arrPriceResult+self.get_price(datapage)
            arrAdressResult = arrAdressResult+self.get_adress(datapage)
            arrTitleResult = arrTitleResult+self.get_title(datapage)
            arrPriceMeterResult = arrPriceMeterResult+self.get_price_meter(datapage)
            arrHrefResult = arrHrefResult+self.get_href(datapage)
            arrIdResult = arrIdResult+self.get_id(datapage)
        self.save_to_xlsx(arrAdressResult=arrAdressResult,arrHrefResult=arrHrefResult,arrIdResult=arrIdResult,arrPriceMeterResult=arrPriceMeterResult,arrPriceResult=arrPriceResult,arrTitleResult=arrTitleResult)


