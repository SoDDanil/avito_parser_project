import pandas as pd
pd.options.mode.chained_assignment = None

#метод для сортировки файла (по цене, по площади, по адресу)
def sort_file(file,numberSort):
    df = pd.read_excel(file)
    if numberSort=='1':
        sorted = df.sort_values(by=["Цена"])
        sorted = sorted.drop(sorted[sorted['Цена за метр']=='None'].index,axis=0)
        sorted.to_excel('buf.xlsx',index=False)
        return "Вот отсортированный файл"
    elif numberSort=='2':
        sorted = df.sort_values(by=["Площадь"])
        sorted = sorted.drop(sorted[sorted['Цена за метр']=='None'].index,axis=0)
        sorted.to_excel('buf.xlsx',index=False)
        return "Вот отсортированный файл"
    elif numberSort=='3':
        sorted = df.sort_values(by=["Адрес"])
        sorted = sorted.drop(sorted[sorted['Цена за метр']=='None'].index,axis=0)
        sorted.to_excel('buf.xlsx',index=False)
        return "Вот отсортированный файл"
    else:
        return "Вы ввели неверный номер сортировки"