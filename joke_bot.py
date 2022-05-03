import telebot
from telebot import types
import requests 
import random
#токен привязывающий бота
bot = telebot.TeleBot('5396222937:AAE1WU3271i7CfA9R8hesnUPAFXFa1NsSQQ') 
#служебные списки
message_list = ['Привет!', 'Привет', 'Здравствуй!', 'Привет', 'Привет!', 'Здравствуй!', 'Привет, я хочу умереть', 'Привет!',  'Привет',  'Здравствуй'] 
blacklist = []
joke_list = ['шутка-минутка', 'шутка-часик'] 
#обработка команды /start - приветствие и клавиатура для управления.
#Вообще я думаю поменять эту штуку немного - сделать приветствие + /help??? надо подумать немного над этим вашим дезигном
@bot.message_handler(commands=['start'])
def start_message (message):
    keyboard = types.InlineKeyboardMarkup()
    key_random_joke = types.InlineKeyboardButton(text='Случайная шутка', callback_data='rand_joke')  
    keyboard.add(key_random_joke)
    key_search_joke_keyword = types.InlineKeyboardButton(text = 'Поиск по ключевым словам', callback_data = 'search_keyword')
    keyboard.add(key_search_joke_keyword)
    key_search_joke_cliche = types.InlineKeyboardButton(text = 'Поиск по шаблону', callback_data = 'search_cliche')
    keyboard.add(key_search_joke_cliche)
    key_hedgehog = types.InlineKeyboardButton(text = 'Анекдот про ёжика', callback_data = 'hedgehog')
    keyboard.add(key_hedgehog)
    #а вообще я люблю "Случаи" Хармса, один даже есть в readme и я думала сюда их добавить. 
    #Но это во-первых, не уважительно к автору, а во вторых это не анекдоты. Хотя гораздо смешнее. Особенно в исполнении моей пассии
    bot.send_message(message.chat.id, message_list[random.randint(0, 9)], reply_markup = keyboard)
   
#обработка команды /blacklist - клавиатура с кнопками
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

#Нет никакой необходимости делать две разные функции для обработки callback но я их разделила чтобы было удобнее работать  
@bot.callback_query_handler(func = lambda call: True)
def main_operator(call):
        if call.data == 'rand_joke':
            bot.send_message (call.message.chat.id, joke_list[random.randint(0,1)])
        elif call.data == 'search_keyword':
            bot.send_message (call.message.chat.id, 'Шутка по ключевым словам В РАЗРАБОТКЕ')
        elif call.data == 'search_cliche':
            bot.send_message (call.message.chat.id, 'Заходит как-то шаблонная шутка в бар, а бармен говорит В РАЗРАБОТКЕ')
        elif call.data == 'hedgehog':
            bot.send_message (call.message.chat.id, 'Жил-был ёжик, научился он дышать попой. Сел на пенёк и задохнулся') #Это единственная шутка которую я могу сходу рассказать.
#Я где-то сломала эту функцию и не могу понять где
def blacklist_operations(call):
        if call.data == 'show_blacklist':
            if len(blacklist) == 0:
                bot.send_message (call.message.chat.id, 'Черный список пустой')
            else:
                bot.send_message (call.message.chat.id, 'Черный список: ' + str(blacklist))
        elif call.data == 'edit_blacklist':
            keyboard_edit = types.InlineKeyboardMarkup()
            key_add_words = types.InlineKeyboardButton(text = 'Добавить', callback_data = 'edit_add')
            keyboard_edit.add(key_add_words)
            key_delete_words = types.InlineKeyboardButton (text = 'Удалить', callback_data = 'delete_word')
            keyboard_edit.add(key_delete_words)
            key_clear_words = types.InlineKeyboardButton (text = 'Очистить чёрный список', callback_data = 'clear_blacklist')
            keyboard_edit.add(key_clear_words)
            bot.send_message (call.message.chat.id, 'Редактирование чёрного списка', reply_markup = keyboard_edit)
#отправка запросов в телегу спрашивать ну как там с (деньгами) сообщениями
bot.polling(non_stop = True)