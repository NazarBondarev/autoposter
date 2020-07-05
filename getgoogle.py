#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json
import schedule
import time
import datetime
import requests
import configuration



r = requests.Session()

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = "1Tg_8hFW_jOvg0gl3fZ6RM_vY8gtFpSWmCgL6-rsNIms"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)


class GetRecord:

    """Инициализируем данные для работы с таблицей"""
    def __init__(self, CREDENTIALS_FILE, spreadsheet_id, credentials, service, values, last_record, r):
        
        self.CREDENTIALS_FILE = CREDENTIALS_FILE
        self.spreadsheet_id = spreadsheet_id
        self.credentials = credentials
        self.service = service
        self.values = values
        self.last_record = last_record
        self.r = r

    """Новая запись в config"""
    def write_new_data(self, value):
        self.value = value
        self.last_record = {"last_record":value[0], 
                            "record_data_1":value[1], 
                            "record_data_2":value[2], 
                            "record_data_3":value[3]}

        with open("./config.json", 'w', encoding="UTF-8") as write_new:
            json.dump(self.last_record, write_new, indent=4, ensure_ascii=False)
    
    """Метод запуска проверки"""
    def checking(self):
        today = datetime.datetime.today()
        if self.values['values'][-1][0] == self.last_record['last_record']:
            return "Новых записей нет: {0}".format(today.strftime("%Y-%m-%d-%H.%M.%S"))

        else:
            print("Новая запись: {0}".format(today.strftime("%Y-%m-%d-%H.%M.%S")))
            GetRecord.write_new_data(self, self.values['values'][-1])            
            text = self.values['values'][-1]
            format_text = "<b>Контакт</b>: {0} ({1})\n\n<b>Задача</b>: {2}".format(text[1], text[2], text[3])

            with open('./chatid.txt', 'r') as read:
                i = read.read()
            self.r.post(f"https://api.telegram.org/bot{configuration.API_TOKEN}/sendMessage", 
                params = {'chat_id':int(i),'text': format_text, 'parse_mode':'html'})

        
#Функция вызывается циклом ниже
def job():
    while True:
        with open('./chatid.txt', 'r') as read:
                i = read.read()

        with open('./config.json', 'r') as read_config:
            last_record = json.load(read_config)

        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range = "A2:E10000",
            majorDimension='ROWS',
                ).execute()
        chceck = GetRecord(CREDENTIALS_FILE, spreadsheet_id, credentials, service, values, last_record, r).checking()
        print(chceck)
        time.sleep(10)
        

job()
