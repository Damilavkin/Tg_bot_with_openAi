import os
import openai
import telebot
from dotenv import load_dotenv
load_dotenv()

# My token
bot = telebot.TeleBot(os.getenv('TOKEN'))
openai.api_key = os.getenv('API_KEY')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi, I'm a bot artist, enter a description of the picture you want to get and I'll draw it for you")


@bot.message_handler(func=lambda _: True)
def send_img(message):
    try:
        response = openai.Image.create(
            prompt=message.text,
            n=1,
            size='512x512',
        )
    except openai.error.InvalidRequestError:
        bot.send_message(chat_id=message.from_user.id, text='It is not possible to generate an image for this request')

    bot.send_photo(chat_id=message.from_user.id, photo=response['data'][0]['url'])


bot.infinity_polling()
