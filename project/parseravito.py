import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
from time import sleep
import pandas as pd
import collections.abc
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
from hyper.contrib import HTTP20Adapter

# класс где записаны все методы парсера
class AvitoParser():
    #метод подключения к сайту
    def connection(self,url):
        s = requests.Session()
        s.mount('https://',  HTTP20Adapter())
        response = s.get(url=url)
        response.encoding = "utf8"
        #если подключение удалось то возвращаем переменную bs4
        if response.status_code==200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        else:
            print('Неудачное соединение код ошибки',response.status_code)
            exit() 

    #метод который получается количество страниц в разделе недвижимость
    def get_count_pages(self,sity):
        url = f'https://www.avito.ru/{sity}/kvartiry/prodam-ASgBAgICAUSSA8YQ?p=1'
        soup = self.connection(url)
        return soup.find_all('span',class_='styles-module-text_size_s-LNY0Q')[-1].text
    
    #метод для получения цены за квартиру 
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

    #метод который возвращает массив адресов с каждой страницы
    def get_adress(self,data):
        arrAdress = []
        for temp in data:
            try:
                adress = temp.find('div',attrs = {'data-marker': 'item-address'}).get_text()
                print(adress)
                arrAdress.append(adress)
            except:
                arrAdress.append("None")
        return arrAdress
    
    #метод который возвращает массив титулов(оглавления объявления) с каждой страницы
    def get_title(self,data):
        arrTitle = []
        for temp in data:
            try:
                title = temp.find(attrs = {'itemprop':'name'}).get_text()
                arrTitle.append(title)
            except:
                arrTitle.append("None")
        return arrTitle
    
    #метод который возвращает массив цен за метр с каждой страницы
    def get_price_meter(self,data):
        arrPriceMeter = []
        for temp in data:
            try:
                priceMeter = temp.find('span',class_='price-noaccent-X6dOy price-normalizedPrice-PplY9 text-text-LurtD text-size-s-BxGpL')
                arrPriceMeter.append(priceMeter.text)
            except:
                arrPriceMeter.append("None")
        for i in range(0,len(arrPriceMeter)):
            try:
                buf = arrPriceMeter[i]
                arrPriceMeter[i] = int(buf.split(' ')[0] + buf.split(' ')[1])
            except:
                arrPriceMeter[i] = 'None'
        return arrPriceMeter
    
    #метод который возвращает массив площади квартир(считается обычной математикой а не с сайта) с каждой страницы
    def get_square_room(self,arrPriceMeter,arrPrice):
        arrSquare = []
        for i in range(0,len(arrPrice)):
            try:
                arrSquare.append(int(arrPrice[i])/int(arrPriceMeter[i]))
            except:
                arrSquare.append('None')
        return arrSquare
    
    #метод который возвращает массив ссылок на квартиры с каждой страницы
    def get_href(self,data):
        arrHref = []
        for temp in data:
            try:
                href = 'https://www.avito.ru' + temp.find('a').get('href')
                arrHref.append(href)
            except:
                arrHref.append("None")
        return arrHref
    
    #метод который возвращает массив id с каждой страницы
    def get_id(self,data):
        arrId = []
        for temp in data:
            try:
                id = temp.get('id')
                arrId.append(id)
            except:
                arrId.append("None")
        return arrId

    #метод который сохраняет данные в эксель
    def save_to_xlsx(self,arrPriceResult,arrAdressResult,arrTitleResult,arrPriceMeterResult,arrHrefResult,arrIdResult,arrSquareResult,sity):
        df = pd.DataFrame({'Цена' : arrPriceResult,
                   'id' : arrIdResult,
                   'Ссылка' : arrHrefResult,
                   'Адрес' : arrAdressResult,
                   'Цена за метр' : arrPriceMeterResult,
                   'Титул' : arrTitleResult,
                   'Площадь': arrSquareResult
                   })
        nameXLSX = self.get_name_xlsx(sity)
        try:
            with open(nameXLSX) as f:
                pass
        except FileNotFoundError:
            # Если файл не существует, создаем пустой датафрейм и сохраняем его в Excel
            dfBuf = pd.DataFrame()
            dfBuf.to_excel(nameXLSX, index=False)
        
        df.to_excel(nameXLSX, index=False)

    #метод для получения текущей даты, которая будет являться именем файла
    def get_name_xlsx(self,sity):
        day = datetime.now().day
        month = datetime.now().month
        if datetime.now().month  < 10: 
            month = '0'+ str(datetime.now().month)
        else:
            month =  str(datetime.now().month)
        if datetime.now().day < 10:
            day = '0' + str(datetime.now().day)
        else:
            day = str(datetime.now().day)
        year = str(datetime.now().year)
        nameXLSX = year + '.' + month + '.' + day +'.' + sity+ '.xlsx'
        return nameXLSX

    #метод для сбора всех данных
    def collect_data(self):
            arrSity = ['zelenodolsk','kazan','moskva','novosibirsk']
            for sity in arrSity:
                print(sity,"---------------")
                countPages = self.get_count_pages(sity)
                print(int(countPages)+1)
                arrSquareResult = []
                arrPriceResult = []
                arrAdressResult = []
                arrTitleResult = []
                arrPriceMeterResult = []
                arrHrefResult = []
                arrIdResult = []
                for page in range(1,int(countPages)+1):
                    sleep(3)
                    print(page,sity)
                    url = f'https://www.avito.ru/{sity}/kvartiry/prodam-ASgBAgICAUSSA8YQ?p={page}'
                    data = self.connection(url)
                    datapage = data.find('div', class_='items-items-kAJAg')
                    arrPriceResult = arrPriceResult+self.get_price(datapage)
                    arrAdressResult = arrAdressResult+self.get_adress(datapage)
                    arrTitleResult = arrTitleResult+self.get_title(datapage)
                    arrPriceMeterResult = arrPriceMeterResult+self.get_price_meter(datapage)
                    arrHrefResult = arrHrefResult+self.get_href(datapage)
                    arrIdResult = arrIdResult+self.get_id(datapage)
                    arrSquareResult =self.get_square_room(arrPriceMeterResult,arrPriceResult)
                    self.save_to_xlsx(arrAdressResult=arrAdressResult,arrHrefResult=arrHrefResult,arrIdResult=arrIdResult,arrPriceMeterResult=arrPriceMeterResult,arrPriceResult=arrPriceResult,arrTitleResult=arrTitleResult,arrSquareResult=arrSquareResult,sity=sity)


