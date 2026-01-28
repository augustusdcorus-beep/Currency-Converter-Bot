import telebot
from telebot import types
import requests
import sqlite3
bot = telebot.TeleBot('')
URL_NBU = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
def set_user_currency(user_id, currency_code):
    db = sqlite3.connect('bot_memory.db')
    cursor = db.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (user_id, currency) VALUES (?, ?)", (user_id, currency_code))
    db.commit()
    db.close()
def get_user_currency(user_id):
    db = sqlite3.connect('bot_memory.db')
    cursor = db.cursor()
    cursor.execute("SELECT currency FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    db.close()
    if result is None:
        return None
    return result[0]
def get_rate_from_nbu(currency_code):
    try:
        response = requests.get(URL_NBU)
        data = response.json()
        for item in data:
            if item['cc'] == currency_code:
                return item['rate']
        return 0
    except:
        return 0
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Хочу Долар")
    btn2 = types.KeyboardButton("Хочу Євро")
    btn3 = types.KeyboardButton("Мій Курс")
    btn4 = types.KeyboardButton("🧮 Калькулятор")
    markup.add(btn1, btn2, btn3, btn4)
    bot.reply_to(message, "Привіт! Обирай дію 👇", reply_markup=markup)
def convert_money(message):
    try:
        uah_amount = float(message.text)
        usd_rate = get_rate_from_nbu("USD")
        eur_rate = get_rate_from_nbu("EUR")
        if usd_rate == 0 or eur_rate == 0:
            bot.reply_to(message, "Помилка банку, не можу порахувати")
            return
        usd_result = round(uah_amount / usd_rate, 2)
        eur_result = round(uah_amount / eur_rate, 2)
        bot.reply_to(message, f"💸 За {uah_amount} грн ти отримаєш:\n\n🇺🇸 {usd_result} USD\n🇪🇺 {eur_result} EUR")
    except ValueError:
        bot.reply_to(message, "Це не число! Спробуй натиснути кнопку ще раз.")
@bot.message_handler(content_types=['text'])
def bot_answer(message):
    user_id = message.from_user.id
    if message.text == "Хочу Долар":
        set_user_currency(user_id, "USD")
        bot.reply_to(message, "Добре! Я запам'ятав: ти стежиш за доларомю")
    elif message.text == "Хочу Євро":
        set_user_currency(user_id, "EUR")
        bot.reply_to(message, "Добре! Я запам'ятав: ти стежиш за євро.")
    elif message.text == "Мій Курс":
        currency = get_user_currency(user_id)
        if currency is None:
            bot.reply_to(message, "Ти ще не обрав валюту! Натисни кнопку вище.")
        else:
            rate = get_rate_from_nbu(currency)
            bot.reply_to(message, f"Курс {currency}: {rate} грн")
    elif message.text == "🧮 Калькулятор":
        msg = bot.reply_to(message, "Введи суму в гривнях (тільки цифри):")
        bot.register_next_step_handler(msg, convert_money)
    else:
        bot.reply_to(message, "Я розумію тільки кнопки.")
print("Бот-калькулятор запущений...")
bot.infinity_polling()

                     