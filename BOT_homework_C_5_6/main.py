import json
import telebot
from config import TOKEN
from utils import ConvertionExeption, CryptoConverter, DeleteAdd


bot = telebot.TeleBot(TOKEN)


choice_list = []


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Доступные команды:\n/help\n' \
           'Конвертация активов:\n/values\n' \
           'Добавить/удалить активы/валюты:\n/delete_add\n' \
           'Посмотреть список активов и валют:\n/list'

    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help_func(message: telebot.types.Message):
    bot_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bot_1.row('/start', '/help', '/values')
    bot_1.row('/delete_add', '/list')
    bot.reply_to(message, "Доступные команды:", reply_markup=bot_1)


@bot.message_handler(commands=['list'])
def keys_list(message):
    with open('keys.json', 'r') as json_file:
        data = json.loads(json_file.read())
    for k, v in data.items():
        bot.send_message(message.chat.id, f'{k} {v}')


@bot.message_handler(commands=['values'])
def quote_func(message: telebot.types.Message):
    with open('quote_button.json', 'r') as json_file:
        quote_button = json.loads(json_file.read())
    bot_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*quote_button)
    text = 'Доступные криптовалюты:'
    availble_crypto = bot.send_message(message.chat.id, text, reply_markup=bot_1)
    bot.register_next_step_handler(availble_crypto, base_func)


def base_func(message):
    choice_list.insert(0, message.text)
    with open('base_button.json', 'r') as json_file:
        base_button = json.loads(json_file.read())
    bot_2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*base_button)
    text = 'Доступные валюты:'
    availble_currency = bot.send_message(message.chat.id, text, reply_markup=bot_2)
    bot.register_next_step_handler(availble_currency, amount_func)


def amount_func(message):
    choice_list.insert(1, message.text)
    text = bot.send_message(message.chat.id, 'Введите количество')
    bot.register_next_step_handler(text, result)


def result(message):
    choice_list.insert(2, message.text)

    try:
        quote, base, amount = choice_list[0], choice_list[1], choice_list[2]
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
        help_func(message)
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        help_func(message)
    else:
        with open('keys.json', 'r') as json_file:
            keys = json.loads(json_file.read())
        text = f'Цена за {amount} {keys[quote]} = {round(float(amount) * total_base, 2)} {keys[base]}'
        bot.reply_to(message, text)
        help_func(message)

    choice_list.clear()


@bot.message_handler(commands=['delete_add'])
def delete_add(message):
    bot_3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bot_3.row('Добавить актив', 'Удалить актив')
    bot_3.row('Добавить валюту', 'Удалить валюту')
    bot_3.row('главное меню')
    a = bot.send_message(message.chat.id, 'Какую операцию хотите произвести?', reply_markup=bot_3)
    bot.register_next_step_handler(a, if_elif)


def if_elif(message):
    if message.text == 'главное меню':
        help_func(message)
    elif message.text == 'Добавить актив':
        a = bot.send_message(message.chat.id, 'Введите название актива которое хотите добавить:\n'
                                              'Формат ввода: <название тикер> через пробел, пример:\n'
                                              'шибаину SHIB')
        bot.register_next_step_handler(a, add_quote_button)
    elif message.text == 'Удалить актив':
        a = bot.send_message(message.chat.id, 'Введите название актива (только название, \
как укахано на кнопке, одним словом) который хотите удалить:')
        bot.register_next_step_handler(a, delete_quote_button)
    elif message.text == 'Добавить валюту':
        a = bot.send_message(message.chat.id, 'Введите название валюты которую хотите добавить:\n'
                                              'Формат ввода: <название тикер> через пробел, пример:\n'
                                              'йена JPY')
        bot.register_next_step_handler(a, add_base_button)
    elif message.text == 'Удалить валюту':
        a = bot.send_message(message.chat.id, 'Введите название валюты (название, \
как укахано на кнопке, одним словом) которую хотите удалить:')
        bot.register_next_step_handler(a, delete_base_button)


def add_quote_button(message):
    if len(message.text.split()) == 2:
        DeleteAdd.add_button(message, 'quote_button.json')
        bot.reply_to(message, f'Актив "{message.text}" добавлен')
    else:
        bot.reply_to(message, f'Не удалось обработать данные "{message.text}"\n'
                              'Формат ввода: <название тикер> через пробел, пример:\n'
                              'шибаину SHIB')
    help_func(message)


def delete_quote_button(message):
    DeleteAdd.delete_button(message, 'quote_button.json')
    bot.reply_to(message, f'Актив "{message.text}" удалён')
    help_func(message)


def add_base_button(message):
    if len(message.text.split()) == 2:
        DeleteAdd.add_button(message, 'base_button.json')
        bot.reply_to(message, f'Валюта "{message.text}" добавлена')
    else:
        bot.reply_to(message, f'Не удалось обработать данные "{message.text}".\n'
                              'Формат ввода: <название тикер> через пробел, пример:\n'
                              'йена JPY')
    help_func(message)


def delete_base_button(message):
    DeleteAdd.delete_button(message, 'base_button.json')
    bot.reply_to(message, f'Валюта "{message.text}" удалена')
    help_func(message)


bot.polling(none_stop=True)
