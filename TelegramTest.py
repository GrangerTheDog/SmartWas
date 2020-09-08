import telebot
from telebot import types


sw_status = False

bot = telebot.TeleBot("1300564024:AAGfIIywVz0d06CxCLvJ6ABP7xKhI7Rt7ek", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Howdy, how are you doing?")
    
@bot.message_handler(commands=['link'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Linking system here [TODO]")
    
    

    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global sw_status
    if "Start SmartWas" in message.text:
        if sw_status is False:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "SmartWas is gestart!", reply_markup=markup)
            sw_status = True
            
        else:
            bot.reply_to(message, "SmartWas staat al aan")
    elif "Stop SmartWas" in message.text:
        if sw_status is True:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "SmartWas is gestopt!", reply_markup=markup)
            sw_status = False
            
        else:
            bot.reply_to(message, "SmartWas staat al uit")    
    elif "Herstart SmartWas" in message.text:
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "SmartWas device word opnieuw opgestart!", reply_markup=markup)
        
    elif "Instructies" in message.text:
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Instructies hier!", reply_markup=markup)
        
    else:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        if sw_status is False:
            itembtn1 = types.KeyboardButton('Start SmartWas')
        else:
            itembtn1 = types.KeyboardButton('Stop SmartWas')   
        itembtn2 = types.KeyboardButton('Instructies')
        itembtn3 = types.KeyboardButton('Herstart SmartWas')
        markup.add(itembtn2, itembtn3, itembtn1)
        bot.send_message(message.chat.id, "Kies een optie:", reply_markup=markup)
    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)
    
    
bot.polling()
