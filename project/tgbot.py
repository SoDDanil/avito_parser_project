import telebot
from telebot import types
import os
from parseravito import AvitoParser

# Создаем объект бота
bot = telebot.TeleBot('6143020140:AAHn9CUxBSCTqcfrkhyO1rJa47xbILRMlXI')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('/help')
    #itembtn2 = types.KeyboardButton('/settings')
    itembtn3 = types.KeyboardButton('/getfile')
    markup.add(itembtn1, itembtn3)
    bot.send_message(message.chat.id, 'Привет, я бот!', reply_markup=markup)


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Я могу помочь тебе вот в чем:')

# Обработчик команды /getfile
@bot.message_handler(commands=['getfile'])
def get_file(message):
    try:
        try: 
            AvitoParser().collect_data()
        except Exception as e:
             bot.send_message(message.chat.id, 'Ошибка при парсинге данных')
        # Открываем файл data.xlsx
        with open('data.xlsx', 'rb') as f:
            # Отправляем файл в чат
            bot.send_document(message.chat.id, f)
    except Exception as e:
        # Отправляем сообщение об ошибке, если файл не найден
        bot.send_message(message.chat.id, 'Ошибка при отправке файла: {}'.format(str(e)))

# Запускаем бота
bot.polling()