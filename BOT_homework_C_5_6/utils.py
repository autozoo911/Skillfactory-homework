import requests
import json


class ConvertionExeption(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        with open('keys.json', 'r') as json_file:
            keys = json.loads(json_file.read())

        if quote == base:
            raise ConvertionExeption(f'Одинаковые активы "{base}" неконвертируемы, проверьте сообщение \
        и попробуйте еще раз \n '
                                     'Формат ввода: \n'
                                     '<актив> <валюта> <количество>')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать тикер "{quote}"\n'
                                     f'Список доступных названий и тикеров можно посмотреть тут:\n/list')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать тикер "{base}"\n'
                                     f'Список доступных названий и тикеров можно посмотреть тут:\n/list')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Не удалось обработать количество "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[base_ticker]

        return total_base


class DeleteAdd:
    @staticmethod
    def add_button(message, file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
            data.append(message.text.split()[0])
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file)

        with open('keys.json') as json_file:
            data = json.load(json_file)
            data[message.text.split()[0]] = message.text.split()[1].upper()
        with open('keys.json', 'w') as json_file:
            json.dump(data, json_file)


    @staticmethod
    def delete_button(message, file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
            if message.text in data:
                data.remove(message.text)
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file)

        with open('keys.json') as j_file:
            keys_data = json.load(j_file)
            if message.text in keys_data.keys():
                del keys_data[message.text]
        with open('keys.json', 'w') as j_file:
            json.dump(keys_data, j_file)
