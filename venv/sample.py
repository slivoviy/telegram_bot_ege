from telegram.ext import Updater         # пакет называется python-telegram-bot, но Python-
from telegram.ext import CommandHandler  # модуль почему-то просто telegram ¯\_(ツ)_/¯

TOKEN = '1027639107:AAGMVghxLvsqHF-36i_y_hk-Nvc0Qn-zak0'
REQUEST_KWARGS={
    'proxy_url': 'socks5://s5.priv.opennetwork.cc:1080',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'v3_470788620',
        'password': 'BJBANUXu',
    }
}

def start(bot, update):
    # подробнее об объекте update: https://core.telegram.org/bots/api#update
    bot.sendMessage(chat_id=update.message.chat_id, text="Здравствуйте.")


updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)  # тут токен, который выдал вам Ботский Отец!

start_handler = CommandHandler('start', start)  # этот обработчик реагирует
                                                # только на команду /start

updater.dispatcher.add_handler(start_handler)   # регистрируем в госреестре обработчиков
updater.start_polling()  # поехали!