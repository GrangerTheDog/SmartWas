#Wasmachine Testing
from sense_hat import SenseHat
from time import sleep
import telebot
from telebot import types
bot = telebot.TeleBot("1300564024:AAGfIIywVz0d06CxCLvJ6ABP7xKhI7Rt7ek", parse_mode=None)

sense = SenseHat()
#CONFIG
timelimit = 180 #3 minuten
telegramid = 447307637

#Default Values
gp = 0
gr = 0
gy = 0
timer = 0


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
    
    #Als de timer de ingestelde seconden heeft bewaart, stuur een berichtje naar telegram en zet de RGB naar groen
    if timelimit <= timer:
        print("Wasmachine zou klaar moeten zijn")
        bot.send_message(telegramid, "Wasmachine is klaar")
        sense.clear(0, 255 ,0) 
        timer = 0
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
    sleep(1)
