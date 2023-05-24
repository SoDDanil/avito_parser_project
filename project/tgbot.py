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

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('помощь')  # Заменяем текст команды /help на "помощь"
    itembtn2 = types.KeyboardButton('отсортированный файл')
    itembtn3 = types.KeyboardButton('сегодняшний файл')
    itembtn4 = types.KeyboardButton('сортировка по критериям')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, 'Привет, я бот!', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'помощь')
def help_message(message):
    bot.send_message(message.chat.id, 'Я могу помочь тебе вот в чем:\n\n1) команда "сегодняшний файл" отправит файл за текущий день\n\n2) команда "отсортированный файл" отправит отсортированный по критериям файл за нужный день (зеленым цветом выделены квартиры на 30% дешевлет средней по рынку, красным квартиры дороже чем средние по рынку на 30%)\n\n3) команда "сортировка по критериям" позволяет отсортировать файл за текущий день')

# Обработчик команды /getsortfile
@bot.message_handler(func=lambda message: message.text == 'отсортированный файл')
def handle_get_sort_file(message):
    get_sort_file(message)

# Получение отсортированного эксель файла
def get_sort_file(message):
    bot.send_message(message.chat.id, "Введите дату в формате гггг.мм.дд (пример 2023.04.21)")
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    date = message.text
    keyboard = get_city_keyboard(date)
    bot.send_message(message.chat.id, "Выберите город:", reply_markup=keyboard)

def get_city_keyboard(date):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text='Зеленодольск', callback_data=f'city_{date}.zelenodolsk'),
        types.InlineKeyboardButton(text='Казань', callback_data=f'city_{date}.kazan'),
        types.InlineKeyboardButton(text='Москва', callback_data=f'city_{date}.moskva'),
        types.InlineKeyboardButton(text='Новосибирск', callback_data=f'city_{date}.novosibirsk')
    ]
    keyboard.add(*buttons)
    return keyboard

# Обработчик команды /getfile
@bot.message_handler(func=lambda message: message.text == 'сегодняшний файл')
def handle_get_file(message):
    get_file(message)

def get_file(message):
    keyboard = get_city_keyboard_today(date=AvitoParser().get_date())
    bot.send_message(message.chat.id, "Выберите город:", reply_markup=keyboard)

def get_city_keyboard_today(date):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text='Зеленодольск', callback_data=f'file_{date}.zelenodolsk'),
        types.InlineKeyboardButton(text='Казань', callback_data=f'file_{date}.kazan'),
        types.InlineKeyboardButton(text='Москва', callback_data=f'file_{date}.moskva'),
        types.InlineKeyboardButton(text='Новосибирск', callback_data=f'file_{date}.novosibirsk')
    ]
    keyboard.add(*buttons)
    return keyboard

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.message:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data.startswith('city_'):
        get_city(call.data[5:], call.message)
    elif call.data.startswith('file_'):
        get_today_file(call.data[5:], call.message)

def get_city(data, message):
    nameFile = data + '.xlsx'
    try:
        with open(nameFile, 'rb') as f:
            sort_doc(f, data[:10:])
            with open("buf.xlsx", 'rb') as f:
                bot.send_document(message.chat.id, f)
    except FileNotFoundError:
        bot.send_message(message.chat.id, f"Файл {nameFile} не найден, ошибка при обработке файла")

def get_today_file(data, message):
    bot.send_message(message.chat.id, f"Открыт файл сегодня {data}.xlsx")
    nameFile = data + '.xlsx'
    try:
        with open(nameFile, 'rb') as f:
            bot.send_document(message.chat.id, f)
    except FileNotFoundError:
        bot.send_message(message.chat.id, f"Файл {nameFile} не найден")
# Обработчик команды /sortbysettings
@bot.message_handler(func=lambda message: message.text == 'сортировка по критериям')
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

#----------------

def runBot():
    bot.polling(none_stop=True)

def cronTask():
    try:
        AvitoParser().collect_data()
    except Exception as e:
        print('Ошибка при парсинге: {}'.format(str(e)))

def runScheluders():
    schedule.every().day.at('01:30').do(cronTask)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    t1 = threading.Thread(target=runBot)
    t2 = threading.Thread(target=runScheluders)
    t1.start()
    t2.start()