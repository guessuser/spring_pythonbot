from ast import Lambda
from multiprocessing import context
import telebot
from telebot import types
import random 
from joke_extra import *

bot = telebot.TeleBot('5396222937:AAE1WU3271i7CfA9R8hesnUPAFXFa1NsSQQ') 

message_list = ['Привет!', 'Привет', 'Здравствуй!', 'Привет', 'Привет!', 'Здравствуй!', 'Привет, я хочу умереть', 'Привет!',  'Привет',  'Здравствуй'] 


context = {}

def get_context(user):
    if not user in context:
        return None
    
    context_name = context[user]
    del context[user] 
    return context_name

def set_context(user, context_name):
    context[user] = context_name



@bot.message_handler(commands=['help'])
def help_message (message):
    bot.send_message(message.chat.id, 'Привет! Это чат-бот юморист который травит сомнительные анекдоты.\nКоманда /start запускает бота и выводит в главное меню.\nКоманда /blacklist вызывает настройки черного списка')

@bot.message_handler(commands=['start'])
def start_message (message):
    keyboard = types.InlineKeyboardMarkup()
    key_random_joke = types.InlineKeyboardButton(text='Случайная шутка', callback_data='rand_joke')  
    keyboard.add(key_random_joke)
    key_search_joke_keyword = types.InlineKeyboardButton(text = 'Поиск по ключевым словам', callback_data = 'search_keyword')
    keyboard.add(key_search_joke_keyword)
    bot.send_message(message.chat.id, random.choice(message_list), reply_markup = keyboard)
   

@bot.message_handler(commands = ['blacklist'])
def blacklist_settings(message):
    keyboard_bl = types.InlineKeyboardMarkup()
    key_show_bl = types.InlineKeyboardButton(text='Посмотреть чёрный список', callback_data='show_blacklist' )
    keyboard_bl.add (key_show_bl)
    key_edit_bl = types.InlineKeyboardButton(text = 'Редактировать чёрный список', callback_data='edit_blacklist')
    keyboard_bl.add(key_edit_bl)
    key_clear_bl = types.InlineKeyboardButton(text = 'Очистить чёрный список', callback_data = 'clear_blacklist')
    keyboard_bl.add(key_clear_bl)
    bot.send_message(message.chat.id, 'Настройки чёрного списка - не влияет на функционал бота', reply_markup = keyboard_bl)

@bot.message_handler(func= lambda call: True)
def func_message(message):
    cxt = get_context(message.chat.id)
    if cxt == 'bl_add':
        update_user_blaklist(message.chat.id, message.text.lower().split())
    else:
        bot.reply_to(message, text= 'what?')

@bot.callback_query_handler(func = lambda call: True)
def main_operator(call):
    if call.data == 'rand_joke':
        bot.send_message (call.message.chat.id, get_joke(user=call.message.chat.id))
    elif call.data == 'search_keyword':
        keyboard_search_keyword = types.InlineKeyboardMarkup() 
        create_button = (lambda name: keyboard_search_keyword.add(types.InlineKeyboardButton(text = name, callback_data = 'search_keyword_' + name)))
        create_button('bar')
        create_button('dad')
        create_button('goose')
        bot.send_message (call.message.chat.id, 'Шутка по ключевым словам', reply_markup=keyboard_search_keyword)
    elif call.data.startswith('search_keyword_'):
        keyword = call.data[15:]
        bot.send_message(call.message.chat.id, get_joke(keyword, user=call.message.chat.id))
    elif call.data == 'hedgehog':
        bot.send_message (call.message.chat.id, 'Жил-был ёжик, научился он дышать попой. Сел на пенёк и задохнулся') #Это единственная шутка которую я могу сходу рассказать.
    
#Дальше блок чёрного списка, раньше был отдельной функцией. 
    elif call.data == 'show_blacklist':
        blacklist = get_user_blacklist(call.message.chat.id)
        if len(blacklist) == 0:
            bot.send_message (call.message.chat.id, 'Черный список пустой')
        else:
            bot.send_message (call.message.chat.id, 'Черный список: ' + ', '.join(blacklist))
    elif call.data == 'edit_blacklist':
        keyboard_edit = types.InlineKeyboardMarkup()
        key_add_words = types.InlineKeyboardButton(text = 'Добавить', callback_data = 'edit_add')
        key_show_bl = types.InlineKeyboardButton(text='Посмотреть чёрный список', callback_data='show_blacklist' )
        keyboard_edit.add (key_show_bl)
        keyboard_edit.add(key_add_words)
        key_clear_words = types.InlineKeyboardButton (text = 'Очистить чёрный список', callback_data = 'clear_blacklist')
        keyboard_edit.add(key_clear_words)
        bot.send_message (call.message.chat.id, 'Редактирование чёрного списка', reply_markup = keyboard_edit)
    elif call.data == 'clear_blacklist':
        clear_user_blacklist(call.message.chat.id)
        bot.send_message (call.message.chat.id, 'Черный список очищен')
    elif call.data == 'edit_add':
        set_context(call.message.chat.id, 'bl_add')
        bot.send_message (call.message.chat.id, 'Добавить слова в черный список В РАЗРАБОТКЕ')
           

bot.polling(non_stop = True)