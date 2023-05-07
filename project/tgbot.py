import telebot
from telebot import types
from parseravito import AvitoParser
import schedule
from sortXLSL import sort_doc
import time
import threading
from sortBySettings import sort_file
from telegram import token

# Создаем объект бота
bot = telebot.TeleBot(token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('/help')
    itembtn2 = types.KeyboardButton('/getsortfile')
    itembtn3 = types.KeyboardButton('/getfile')
    itembtn4 = types.KeyboardButton('/sortbysettings')
    markup.add(itembtn1,itembtn2,itembtn3,itembtn4)
    bot.send_message(message.chat.id, 'Привет, я бот!', reply_markup=markup)


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Я могу помочь тебе вот в чем: \n\n 1) команда /getfile отправит файл за текущий день \n\n 2) команда /getsortfile отправит отсортированный по критериям файл за нужный день(зеленым цветом выделены выгодные квартиры, красным невыгодные) \n\n 3)команда /sortbysettings позволяет отсортировать файл за текущий день')

# Обработчик команды /getsortfile
@bot.message_handler(commands=['getsortfile'])
def handle_get_sort_file(message):
    get_sort_file(message)

# Получение отсортированного эксель файла
def get_sort_file(message):
    bot.send_message(message.chat.id, "Введите дату в формате гггг.мм.дд (пример 2023.04.21)")
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    date = message.text
    bot.send_message(message.chat.id, "Выберите город: \n1) Зеленодольск\n2) Казань\n3) Москва\n4) Новосибирск\n\n(Введите цифру соответствующую городу)")
    bot.register_next_step_handler(message, lambda city_message: get_city(city_message, date))

def get_city(city_message, date):
    city = city_message.text
    if city=='1':
        name_file = f"{date}.zelenodolsk.xlsx"
        try:
            with open(name_file, 'rb') as file:
                arrPrice = sort_doc(file)
                with open("buf.xlsx", 'rb') as file1:
                    bot.send_document(city_message.chat.id, file1)
                    bot.send_message(city_message.chat.id, f"Вот файл {name_file}")
        except FileNotFoundError:
            bot.send_message(city_message.chat.id, f"Файл {name_file} не найден")
            get_sort_file(city_message)
    elif city=='2':
        name_file = f"{date}.kazan.xlsx"
        try:
            with open(name_file, 'rb') as file:
                arrPrice = sort_doc(file)
                with open("buf.xlsx", 'rb') as file1:
                    bot.send_document(city_message.chat.id, file1)
                    bot.send_message(city_message.chat.id, f"Вот файл {name_file}")
        except FileNotFoundError:
            bot.send_message(city_message.chat.id, f"Файл {name_file} не найден")
            get_sort_file(city_message)
    elif city=='3':
        name_file = f"{date}.moskva.xlsx"
        try:
            with open(name_file, 'rb') as file:
                arrPrice = sort_doc(file)
                with open("buf.xlsx", 'rb') as file1:
                    bot.send_document(city_message.chat.id, file1)
                    bot.send_message(city_message.chat.id, f"Вот файл {name_file}")
        except FileNotFoundError:
            bot.send_message(city_message.chat.id, f"Файл {name_file} не найден")
            get_sort_file(city_message)
    elif city=='4':
        name_file = f"{date}.novosibirsk.xlsx"
        try:
            with open(name_file, 'rb') as file:
                arrPrice = sort_doc(file)
                with open("buf.xlsx", 'rb') as file1:
                    bot.send_document(city_message.chat.id, file1)
                    bot.send_message(city_message.chat.id, f"Вот файл {name_file}")
        except FileNotFoundError:
            bot.send_message(city_message.chat.id, f"Файл {name_file} не найден")
            get_sort_file(city_message)
    else:
        bot.send_message(city_message.chat.id, "Неверный номер города")
        get_sort_file(city_message)


         

#сортировки разными методами 
# Обработчик команды /sortbysettings
@bot.message_handler(commands=['sortbysettings'])
def get_sort_file_by_settings(message):
    get_sort_file_settings(message)   


def get_sort_file_settings(message):
    bot.send_message(message.chat.id,"Выберите по какому критерию вы бы хотели отсортировать файл: \n 1) По цене \n 2) По площади \n 3) По адресу")
    bot.send_message(message.chat.id,"Для выбора необходимо написать номер нужной сортировки")
    bot.register_next_step_handler(message, get_file_sort)

def get_file_sort(message):
    try:
        arr_sity = ['zelenodolsk','kazan','moskva','novosibirsk']
        for sity in arr_sity:
            nameXLSL = AvitoParser().get_name_xlsx(sity)
            with open(nameXLSL, 'rb') as f:
                otvet = sort_file(file=f,numberSort=message.text)
                if otvet == "Вот отсортированный файл":
                    try:
                        with open('buf.xlsx','rb') as f1:
                            bot.send_message(message.chat.id,f"{otvet} за город {sity}")
                            bot.send_document(message.chat.id, f1)
                    
                    except Exception as e:
                        bot.send_message(message.chat.id, 'Ошибка при отправке файла: {}'.format(str(e)))
                else:
                    bot.send_message(message.chat.id,otvet)
    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка при отправке файла: {}'.format(str(e)))
        

#-----------------
# Обработчик команды /getfile
@bot.message_handler(commands=['getfile'])
def get_file(message):
    bot.send_message(message.chat.id,"Выберите город: \n 1) Зеленодольск \n 2) Казань \n 3) Москва \n 4) Новосибирск \n\n (Необходимо ввести цифру)")
    bot.register_next_step_handler(message, get_file_sity)

def get_file_sity(message):
    numberSity = message.text
    if numberSity=='1':
        sity = 'zelenodolsk'
        nameFile = AvitoParser().get_name_xlsx(sity=sity)
        try:
            with open (nameFile,'rb') as f:
                bot.send_document(message.chat.id,f)
        except Exception as e:
            bot.send_message(message.chat.id, 'Ошибка при отправке файла: {}'.format(str(e)))
    elif numberSity=='2':
        sity = 'kazan'
        nameFile = AvitoParser().get_name_xlsx(sity=sity)
        try:
            with open (nameFile,'rb') as f:
                bot.send_document(message.chat.id,f)
        except Exception as e:
            bot.send_message(message.chat.id, 'Ошибка при отправке файла: {}'.format(str(e)))
    elif numberSity=='3':
        sity = 'moskva'
        nameFile = AvitoParser().get_name_xlsx(sity=sity)
        try:
            with open (nameFile,'rb') as f:
                bot.send_document(message.chat.id,f)
        except Exception as e:
            bot.send_message(message.chat.id, 'Ошибка при отправке файла: {}'.format(str(e)))
    elif numberSity=='4':
        sity = 'novosibirsk'
        nameFile = AvitoParser().get_name_xlsx(sity=sity)
        try:
            with open (nameFile,'rb') as f:
                bot.send_document(message.chat.id,f)
        except Exception as e:
            bot.send_message(message.chat.id, 'Ошибка при отправке файла: {}'.format(str(e)))
    else:
        bot.send_message(message.chat.id,"Вы ввели неверный номер города")
#----------------

def runBot():
    bot.polling(none_stop=True)

def cronTask():
    try:
        AvitoParser().collect_data()
    except Exception as e:
            print('Ошибка при парсинге: {}'.format(str(e)))

def runScheluders():
    schedule.every().day.at('12:05').do(cronTask)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__=='__main__':
    t1 = threading.Thread(target=runBot)
    t2 = threading.Thread(target=runScheluders)
    t1.start()
    t2.start()
