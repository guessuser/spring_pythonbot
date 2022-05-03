from email import message
import telebot
from telebot import types
import requests
import random

bot = telebot.TeleBot('5396222937:AAE1WU3271i7CfA9R8hesnUPAFXFa1NsSQQ')
message_list = ['Привет!', 'Привет', 'Здравствуй!', 'Привет', 'Привет!', 'Здравствуй!', 'Привет, я хочу умереть', 'Привет!',  'Привет',  'Здравствуй']
@bot.message_handler(commands=['start'])
def start_message (message):
    bot.send_message(message.chat.id, message_list[random.randint(0, 9)])
@bot.message_handler(commands = ['blacklist'])
def blacklist_func (message):
    bot.send_message(message.chat.id, 'Настройки черного списка')

bot.polling(non_stop = True)