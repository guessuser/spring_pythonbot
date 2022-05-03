from email import message
import telebot
from telebot import types
import requests
import random

bot = telebot.TeleBot('5396222937:AAE1WU3271i7CfA9R8hesnUPAFXFa1NsSQQ')
message_list = ['Привет!', 'Привет', 'Здравствуй!', 'Привет', 'Привет!', 'Здравствуй!', 'Привет, я хочу умереть', 'Привет!',  'Привет',  'Здравствуй']
blacklist = []
joke_list = ['шутка-минутка', 'шутка-часик']

@bot.message_handler(commands=['start'])
def start_message (message):
    keyboard = types.InlineKeyboardMarkup()
    key_random_joke = types.InlineKeyboardButton(text='Случайная шутка', callback_data='rand_joke')  
    keyboard.add(key_random_joke)
    key_search_joke_keyword = types.InlineKeyboardButton(text = 'Поиск по ключевым словам', callback_data = 'search_keyword')
    keyboard.add(key_search_joke_keyword)
    key_search_joke_cliche = types.InlineKeyboardButton(text = 'Поиск по шаблону', callback_data = 'search_cliche')
    keyboard.add(key_search_joke_cliche)
    bot.send_message(message.chat.id, message_list[random.randint(0, 9)], reply_markup = keyboard)
    def random_joke(call):
        if call.data == 'rand_joke':
            bot.send_message (message.chat.id, joke_list[random.randint(0,1)])

@bot.message_handler(commands = ['blacklist'])
def blacklist_settings(message):
    keyboard_bl = types.InlineKeyboardMarkup()
    key_show_bl = types.InlineKeyboardButton(text='Посмотреть чёрный список', callback_data='show_blacklist' )
    keyboard_bl.add (key_show_bl)
    key_edit_bl = types.InlineKeyboardButton(text = 'Редактировать чёрный список', callback_data='edit_blacklist')
    keyboard_bl.add(key_edit_bl)
    key_clear_bl = types.InlineKeyboardButton(text = 'Очистить чёрный список', callback_data = 'clear_blacklist')
    keyboard_bl.add(key_clear_bl)
    bot.send_message(message.chat.id, 'Настройки чёрного списка', reply_markup = keyboard_bl)
    
@bot.callback_query_handler(func = lambda call: True)
def show_blacklist(call):
        if call.data == 'show_blacklist':
            if len(blacklist) == 0:
                bot.send_message (call.message.chat.id, 'Черный список пустой')
            else:
                bot.send_message (call.message.chat.id, 'Черный список: ' + str(blacklist))
bot.polling(non_stop = True)