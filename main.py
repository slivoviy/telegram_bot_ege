import random

import telegram
import time
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler, RegexHandler
import logging
from functools import wraps
import dictionaries

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

MAIN, STATISTICS, CHOOSESUBJECT, CHOOSETASK, SOLVETASK, RIGHTANSWER, WRONGANSWER, SOLVE, NEXTTASK, TEST = range(10)

tasks = dictionaries.dictionary['информатика'].inf_tasks
answers = dictionaries.dictionary['информатика'].inf_answer
solves = dictionaries.dictionary['информатика'].inf_solves

correct_word = 0


def start(bot, update):
    custom_keyboard = [['Решение задач'], ['Личная статистика']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text='Здравствуйте! Этот бот поможет вам подготовиться к первой '
                                                          'части ЕГЭ по информатике. Чтобы начать решать задания, '
                                                          'нажмите "Решение задач". \n\n Все задания взяты с ресурса '
                                                          'https://inf-ege.sdamgia.ru/', reply_markup=reply_markup)
    return TEST


def maain(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Выберите действие:')
    return TEST


def test(bot, update):
    if update.message.text == 'Решение задач':
        custom_keyboard = [['Информатика'], ['Математика']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text='Выберите предмет:', reply_markup=reply_markup)
        return CHOOSESUBJECT
    else:
        bot.send_message(chat_id=update.message.chat_id, text='В разработке :)')


def choose_subject(bot, update):
    global tasks
    global answers
    global solves

    if update.message.text == 'Информатика':
        tasks = dictionaries.dictionary['информатика'].inf_tasks
        answers = dictionaries.dictionary['информатика'].inf_answer
        solves = dictionaries.dictionary['информатика'].inf_solves
        bot.send_message(chat_id=update.message.chat_id, text='Напишите номер задания (от 1 до 23)',
                         parse_mode=telegram.ParseMode.MARKDOWN)
        return CHOOSETASK
    else:
        tasks = dictionaries.dictionary['математика'].mat_tasks
        answers = dictionaries.dictionary['математика'].mat_answer
        solves = dictionaries.dictionary['математика'].mat_solves
        bot.send_message(chat_id=update.message.chat_id, text='Напишите номер задания (от 1 до 23)',
                         parse_mode=telegram.ParseMode.MARKDOWN)
        return CHOOSETASK


def choose_task(bot, update):
    task_number = update.message.text
    if not task_number.isdigit():
        bot.send_message(chat_id=update.message.chat_id, text='Вы ввели не число! Введите число от 1 до 23')
        return CHOOSETASK
    if not 23 >= int(task_number) >= 1:
        bot.send_message(chat_id=update.message.chat_id, text='Число не входит в рамки! Введите число от 1 до 23')
        return CHOOSETASK

    num = random.randint(1, len(tasks) - 1)
    bot.send_message(chat_id=update.message.chat_id, text=tasks[num], parse_mode=telegram.ParseMode.MARKDOWN)
    global correct_word
    correct_word = num
    return SOLVETASK


def statistics(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='В разработке :)')
    return MAIN


def solve_task(bot, update):
    if update.message.text == answers[correct_word]:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Правильно, молодец! Хотите решить ещё одну задачу? (ответьте да/нет)')
        return NEXTTASK
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Боюсь, это неверный ответ. Правильный ответ: ' + answers[
            correct_word] + '.Хотите увидеть решение? (ответьте да/нет)')
        return SOLVE


# def wrong_answer(bot, update):
#
#
#
# def right_answer(bot, update):



def solve(bot, update):
    answer = update.message.text.lower()
    if answer != 'да' and answer != 'нет':
        bot.send_message(chat_id=update.message.chat_id, text='Не понимаю ваш ответ. Напишите да или нет')
        return SOLVE
    if answer == 'да':
        bot.send_message(chat_id=update.message.chat_id, text=solves[correct_word])
        time.sleep(4)
    bot.send_message(chat_id=update.message.chat_id, text='Хотите решить ещё одну задачу?')
    return NEXTTASK


def next_task(bot, update):
    answer = update.message.text.lower()
    if answer != 'да' and answer != 'нет':
        bot.send_message(chat_id=update.message.chat_id, text='Не понимаю ваш ответ. Напишите да или нет')
        return NEXTTASK
    if answer == 'да':
        custom_keyboard = [['Информатика'], ['Математика']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text='Выберите предмет:', reply_markup=reply_markup)
        return CHOOSESUBJECT
    else:
        custom_keyboard = [['Решение задач'], ['Личная статистика']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text='Выберите действие:', reply_markup=reply_markup)
        return TEST


def cancel(bot, update):
    return ConversationHandler.END


def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)

        return command_func

    return decorator


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    token = '1027639107:AAGMVghxLvsqHF-36i_y_hk-Nvc0Qn-zak0'
    request_kwargs = {
        'proxy_url': 'socks5://s5.priv.opennetwork.cc:1080',
        'urllib3_proxy_kwargs': {
            'username': 'v3_470788620',
            'password': 'BJBANUXu',
        }
    }

    updater = Updater(token, request_kwargs=request_kwargs)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN: [MessageHandler(Filters.text, maain)],
            STATISTICS: [MessageHandler(Filters.text, statistics)],
            CHOOSESUBJECT: [MessageHandler(Filters.text, choose_subject)],
            CHOOSETASK: [MessageHandler(Filters.text, choose_task)],
            SOLVETASK: [MessageHandler(Filters.text, solve_task)],
            # RIGHTANSWER: [MessageHandler(Filters.text, right_answer)],
            # WRONGANSWER: [MessageHandler(Filters.text, wrong_answer)],
            SOLVE: [MessageHandler(Filters.text, solve)],
            NEXTTASK: [MessageHandler(Filters.text, next_task)],
            TEST: [MessageHandler(Filters.text, test)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
