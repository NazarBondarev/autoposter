#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import configuration
from telebot import types
import requests
import time
import schedule



r = requests.Session()
url = f'https://api.telegram.org/bot{configuration.API_TOKEN}/sendMessage'
API_TOKEN = configuration.API_TOKEN


bot = telebot.TeleBot(API_TOKEN)
CHAT_ID = configuration.load_new_id()

@bot.message_handler(commands = ['changeid'])
def changeid(message):
        if message.from_user.id in configuration.ADMINS and message.chat.type == 'group' or message.chat.type == 'supergroup':
            result = r.post(url, params ={'chat_id': int(message.chat.id), 
            'text':'Переезжаю в этот чат'})
            with open('./chatid.txt', 'w') as write_new_id:
                write_new_id.write(str(message.chat.id))
                configuration.load_new_id()


bot.infinity_polling(none_stop=True)

