#! /usr/bin/python3
#Wasmachine Testing
from sense_hat import SenseHat
from time import sleep
import telebot
from telebot import types
bot = telebot.TeleBot("1300564024:AAGfIIywVz0d06CxCLvJ6ABP7xKhI7Rt7ek", parse_mode=None)

sense = SenseHat()
sense.low_light = True
sense.clear(0, 0 ,255) 
#CONFIG
timelimit = 300 #3 minuten
telegramid = 447307637

#Global Vars
sw_status = False
timelimit = timelimit * 10

def startWas():
    #Default Values
    global sw_status
    gp = 0
    gr = 0
    gy = 0
    timer = 0
    if sw_status is False:
        sw_status = True
        bot.send_message(telegramid, "Wasmachine staat aan")

        while True:
            gyro_only = sense.get_gyroscope()
            #Berekent het gemiddelde van de vorige values en de huidige values
            dp = gp - gyro_only["pitch"]
            dr = gr - gyro_only["roll"]
            dy = gy - gyro_only["yaw"]
            #Slaat de huidige values op voor de volgende loop
            gp = gyro_only["pitch"]
            gr = gyro_only["roll"]
            gy = gyro_only["yaw"]
            
            #Debug verschil
            #print(dp)
            #print(dr)
            #print(dy)
            if sw_status is False:
                print("Wasmachine Detectie uitgeschakeld")
                bot.send_message(telegramid, "Wasmachine Detectie uitgeschakeld")
                sense.clear(0, 0, 255)
                break;
                
            #Als de timer de ingestelde seconden heeft bewaart, stuur een berichtje naar telegram en zet de RGB naar groen
            if timelimit <= timer:
                print("Wasmachine zou klaar moeten zijn")
                markup = types.ReplyKeyboardMarkup(row_width=2)
                itembtn1 = types.KeyboardButton('Start SmartWas')   
                itembtn2 = types.KeyboardButton('Instructies')
                itembtn3 = types.KeyboardButton('Herstart SmartWas')
                markup.add(itembtn2, itembtn3, itembtn1)

                bot.send_message(telegramid, "Wasmachine is klaar", reply_markup=markup)
                sense.clear(0, 255 ,0) 
                timer = 0
                sw_status = False
                break;
            #Als het verschil kleiner is dan 2, voeg 1 bij timer [Pas aan per wasmachine!]
            if -2 < dp < 2 and -2 < dr < 2 and -2 < dy < 2 :
                timer = timer + 1
                print("Low difference! ", timer)
                sense.clear(255, 165 ,0) 
            #Er is beweging dus reset de timer
            else:
                print("Is moving reseting timer!")
                sense.clear(255, 0 ,0) 
                timer = 0
            sleep(0.1)

    else:
        bot.send_message(telegramid, "SmartWas draait al")




@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.chat.id is not telegramid:
        global sw_status
        markup = types.ReplyKeyboardMarkup(row_width=2)
        if sw_status is False:
            itembtn1 = types.KeyboardButton('Start SmartWas')
        else:
            itembtn1 = types.KeyboardButton('Stop SmartWas')   
        itembtn2 = types.KeyboardButton('Instructies')
        itembtn3 = types.KeyboardButton('Herstart SmartWas')
        markup.add(itembtn2, itembtn3, itembtn1)

        if "Start SmartWas" in message.text:
            if sw_status is False:
                markup = types.ReplyKeyboardMarkup(row_width=2)
                itembtn1 = types.KeyboardButton('Stop SmartWas')   
                itembtn2 = types.KeyboardButton('Instructies')
                itembtn3 = types.KeyboardButton('Herstart SmartWas')
                markup.add(itembtn2, itembtn3, itembtn1)
                bot.send_message(message.chat.id, "SmartWas is gestart!", reply_markup=markup)
                startWas()
                
            else:
                bot.send_message(message.chat.id, "SmartWas staat al aan", reply_markup=markup)
        elif "Stop SmartWas" in message.text:
            if sw_status is True:
                markup = types.ReplyKeyboardMarkup(row_width=2)
                itembtn1 = types.KeyboardButton('Start SmartWas')   
                itembtn2 = types.KeyboardButton('Instructies')
                itembtn3 = types.KeyboardButton('Herstart SmartWas')
                markup.add(itembtn2, itembtn3, itembtn1)
                bot.send_message(message.chat.id, "SmartWas is gestopt!", reply_markup=markup)
                sw_status = False
                
            else:
                bot.send_message(message.chat.id, "SmartWas staat al uit", reply_markup=markup)    
        elif "Herstart SmartWas" in message.text:
            bot.send_message(message.chat.id, "SmartWas device word opnieuw opgestart!", reply_markup=markup)
            
        elif "Instructies" in message.text:
            bot.send_message(message.chat.id, "Instructies hier!", reply_markup=markup)
            
        else:
             bot.send_message(message.chat.id, "Kies een optie:", reply_markup=markup)
        
    else:
        bot.send_message(message.chat.id, "Haal nu je eigen SmartWas bij Windesheim! [User not connected to a SmarWas Device]") 

bot.polling()


