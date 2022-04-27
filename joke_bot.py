import telebot

bot = telebot.TeleBot('5396222937:AAE1WU3271i7CfA9R8hesnUPAFXFa1NsSQQ')
@bot.message_handler(commands=['start'])
def start_message (message):
    bot.send_message(message.chat.id, 'hello')
bot.polling(non_stop = True)
