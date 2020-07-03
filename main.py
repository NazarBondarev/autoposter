import telebot
import configuration



bot = telebot.TeleBot(configuration.API_TOKEN)
CHAT_ID = configuration.CHAT_ID



@bot.message_handler(content_types = ['text'])
def send_in_channel(CHAT_ID, text):
    format_text = f"<b>Контакт</b>: {text[2]}\n<b>Задача</b>: {text[3]}"
    bot.send_message(CHAT_ID, format_text, parse_mode = 'html')