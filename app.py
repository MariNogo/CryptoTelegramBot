import telebot
from config import TOKEN, keys, main_menu, help
from extensions import APIException, ValueConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['menu'])
def main_menu(message):
    bot.send_message(message.chat.id, main_menu)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтоб начать введите команду боту в следующем формате:\n<имя валюты> \ \
<в какую валюту перевести>\
<количество переводимой валюты>n\Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
      text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert_result(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много или слишком мало параметров')

        base, quote, amount = values
        total_base = ValueConverter.convert(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        amount = int(amount)
        if amount >=1:
            total_base = str(float(amount * total_base))
        text = f'Цена {amount} {quote} в {base}) - {total_base}'
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "/menu")

bot.polling()
