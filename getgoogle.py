from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import json
import schedule
import time
import main
import datetime


CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = "1DCg-nMtgiJ9BZkXBWmtrD7qieMKQx6YB65bJ-gwRVVs"
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']
            )

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) 


class GetRecord:

    """Инициализируем данные для работы с таблицей"""
    def __init__(self, CREDENTIALS_FILE, spreadsheet_id, credentials, httpAuth, service, values, last_record):
        
        self.CREDENTIALS_FILE = CREDENTIALS_FILE
        self.spreadsheet_id = spreadsheet_id
        self.credentials = credentials
        self.httpAuth = httpAuth
        self.service = service
        self.values = values
        self.last_record = last_record

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
            main.send_in_channel(main.CHAT_ID, self.values['values'][-1])

        

#Функция вызывается циклом ниже
def job():
    with open('./config.json', 'r', encoding='UTF-8') as read_config:
        last_record = json.load(read_config)

    values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range = "A2:E1000",
            majorDimension='ROWS',
                ).execute()
    
    chceck = GetRecord(CREDENTIALS_FILE, spreadsheet_id, credentials, httpAuth, service, values, last_record).checking()
    print(chceck)

#Запуск цикла
schedule.every(5).to(10).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
        
