import requests

r = requests.Session()

url = 'https://api.telegram.org/bot1112434222:AAFYMLOVImWGuNgxwF24abp7dm90SBYOqqI/sendMessage'

result = r.get(url, params =('id'))

print(result)

