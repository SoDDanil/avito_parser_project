import pandas as pd
pd.options.mode.chained_assignment = None

#метод для специально сортировки
def sort_doc(file):
    df = pd.read_excel(file)
    sorted = df.sort_values(by=["Титул"])
    count1k = count2k = count3k = count4k =count5k = countStudio = 0
    sorted = sorted.drop(sorted[sorted['Цена за метр']=='None'].index,axis=0)
    sorted["Комнаты"]=''
    for columnName,columnTitul in sorted['Титул'].items():
        if ('1-к' in columnTitul):
            sorted['Комнаты'][columnName]='1'
            count1k+=1
        if ('2-к' in columnTitul):
            sorted['Комнаты'][columnName]='2'
            count2k+=1
        if ('3-к' in columnTitul):
            sorted['Комнаты'][columnName]='3'
            count3k+=1
        if ('4-к' in columnTitul):
            sorted['Комнаты'][columnName]='4'
            count4k+=1
        if ('5-к' in columnTitul):
            sorted['Комнаты'][columnName]='5'
            count5k+=1
        if ('студия' in columnTitul):
            sorted['Комнаты'][columnName]='студия'
            countStudio+=1
    index1 = int(count1k)
    index2 = index1+int(count2k)
    index3 = index2+int(count3k)
    index4 = index3+int(count4k)
    index5 = index4+int(count5k)
    indexstudio = index5+int(countStudio)
    sorted['Цена за метр'] = sorted['Цена за метр'].astype(float)
    arrAvgPrice = return_avg_price(index1,index2,index3,index4,index5,indexstudio,sorted)
    sorted.to_excel('buf.xlsx',index=False)
    get_count_etag()
    add_price(arrAvgPrice)
    bg_color_dataframe(arrAvgPrice)

#метод для расчета средней цены
def return_avg_price(c1,c2,c3,c4,c5,cstud,df):  
    meanPrice1 = df.iloc[0:c1-1,4].mean()
    meanPrice2 = df.iloc[c1-1:c2-1,4].mean()   
    meanPrice3 = df.iloc[c2-1:c3-1,4].mean()
    meanPrice4 = df.iloc[c3-1:c4-1,4].mean()
    meanPrice5 = df.iloc[c4-1:c5-1,4].mean()
    meanPriceStudio = df.iloc[c5-1:cstud-1,4].mean()
    arrAvgPrice = [meanPrice1,meanPrice2,meanPrice3,meanPrice4,meanPrice5,meanPriceStudio]
    return arrAvgPrice

#метод для получение из титула количества этажей
def get_count_etag():
        df = pd.read_excel('buf.xlsx')
        arr = list(df.iloc[:,5])
        for i in range(0,len(arr)):
            if int(arr[i][arr[i].find('/')+1:arr[i].find('/')+3:])>=10:
                arr[i]=arr[i][arr[i].find('/')+1:arr[i].find('/')+3:]
            else:
                arr[i]=arr[i][arr[i].find('/')+1:arr[i].find('/')+2:]
        df['Этажность']=arr
        df = df.drop_duplicates(subset=["id"])
        sorted = df.sort_values(by=["Комнаты","Адрес","Этажность","Цена за метр"])
        sorted.to_excel('buf.xlsx',index=False)

#метод для добавления средней цены квартир в таблицу
def add_price(arr):
    df = pd.read_excel('buf.xlsx')
    df.at[4,10]='1-комн'
    df.at[5,10]=arr[0]
    df.at[4,11]='2-комн'
    df.at[5,11]=arr[1]
    df.at[4,12]='3-комн'
    df.at[5,12]=arr[2]
    df.at[4,13]='4-комн'
    df.at[5,13]=arr[3]
    df.at[4,14]='5-комн'
    df.at[5,14]=arr[4]
    df.at[4,15]='Студия'
    df.at[5,15]=arr[5]
    df.to_excel('buf.xlsx',index=False)

#метод для выделения зеленым цветом выгодных квартир и красным невыгодных 
def bg_color_dataframe(arrAvgPrice):
    df = pd.read_excel('buf.xlsx')
    small_area=df[df['Площадь']<25]
    df =df[df['Площадь']>25]
    df = pd.concat([df,small_area])
    def highlight_cells(row):
        price, rooms = row['Цена за метр'], row['Комнаты']
        if rooms =='1':
            if price < arrAvgPrice[0]*0.7 :
                return ['background-color: green']*2
            elif price > arrAvgPrice[0]*1.3 :
                return ['background-color: red']*2
            else:
                return [None, None]
        elif rooms =='2':
            if price < arrAvgPrice[1]*0.7 :
                return ['background-color: green']*2
            elif price > arrAvgPrice[1]*1.3 :
                return ['background-color: red']*2
            else:
                return [None, None]
        elif rooms =='3':
            if price < arrAvgPrice[2]*0.7 :
                return ['background-color: green']*2
            elif price > arrAvgPrice[2]*1.3 :
                return ['background-color: red']*2
            else:
                return [None, None]
        elif rooms =='4':
            if price < arrAvgPrice[3]*0.7 :
                return ['background-color: green']*2
            elif price > arrAvgPrice[3]*1.3 :
                return ['background-color: red']*2
            else:
                return [None, None]
        elif rooms =='5':
            if price < arrAvgPrice[4]*0.7 :
                return ['background-color: green']*2
            elif price > arrAvgPrice[4]*1.3 :
                return ['background-color: red']*2
            else:
                return [None, None]
        elif rooms=='студия':
            if price < arrAvgPrice[5]*0.7 :
                return ['background-color: green']*2
            elif price > arrAvgPrice[5]*1.3 :
                return ['background-color: red']*2
            else:
                return [None, None]
    styled = df.style.apply(highlight_cells, subset=['Цена за метр', 'Комнаты'], axis=1)
    styled.to_excel('buf.xlsx', index=False)

