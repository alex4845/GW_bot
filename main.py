import sqlite3
import time
import telebot
from telebot import types

bot = telebot.TeleBot('6359215449:AAH9BymlzQks5ijofQWnkhOLgDliOTDM6H4')

def telegramm_base(connection):
    conn = sqlite3.connect('greenway_bese.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS list_1 (
    number INTEGER PRIMARY KEY, name TEXT (30), city TEXT (30), username TEXT (30),
     user_id INTEGER (20), phone TEXT (20), connection TEXT (20)
     )""")
    cursor.execute('INSERT INTO list_1 (name, city, username, user_id, phone, connection) VALUES (?,?,?,?,?,?)',
                   (name, city, username, user_id, phone, connection))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.send_message(message.from_user.id, "Всем привет!!!🌟🌟🌟 Начнем знакомство! Меня зовут Татьяна, мне 35."
                                           " И я занимаюсь онлайн-бизнесом уже 1,5 года. "
                                           "Что мне нравится в этом бизнесе - это доступность, тебе не надо"
                                           " арендовать помещение, платить деньги за большое количество курсов, "
                                           "чтобы открыть свое дело. У НАС все легально, а также, огромный жирный плюс-"
                                           " бесплатное обучение, на постоянной основе ----- ВСЕГДА!")
    time.sleep(8)
    bot.send_message(message.from_user.id, "Здесь ты сможешь заработать свои первые деньги, а также, и неприлично много,"
                                           " если постараешься. ")
    time.sleep(5)
    keyboard = types.InlineKeyboardMarkup()
    key_swap = types.InlineKeyboardButton(text='Далее', callback_data='swap')
    keyboard.add(key_swap)

    bot.send_message(message.from_user.id, text="Ты получишь азы многих сфер (психология, маркетинг,"
                                           " бизнес-мышление), бесплатно. Прокачаешься, в конце концов, как достойная"
                                           " личность!    🙌✔️👩‍💻"
                     , reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global user_id
    user_id = message.chat.id
    global username
    username = message.chat.username
    if message.text == "📋 Регистрация":
        conn = sqlite3.connect('greenway_bese.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM list_1 WHERE user_id = ?", (user_id,))
        res = cursor.fetchall()
        if res:
            bot.send_message(message.from_user.id, "Вы уже зарегистрированы")
        else:
            bot.send_message(message.from_user.id, "Твое имя или логин?")
            bot.register_next_step_handler(message, get_name)
    elif message.text == "😎 Для админа":
        if user_id == 469632258 or user_id == 1772877481:
            bot.send_message(message.from_user.id, "С какого номера записи показывать?")
            bot.register_next_step_handler(message, get_number1)
        else:
            bot.send_message(message.from_user.id, "Сорри, вы не админ")

def get_number1(message):
    number1 = message.text
    bot.send_message(message.from_user.id, "По какой номер? (если до конца - поставьте '+')")
    bot.register_next_step_handler(message, get_number2, number1)

def get_number2(message, number1):
    conn = sqlite3.connect('greenway_bese.db')
    cursor = conn.cursor()
    number2 = message.text
    if number2 == "+":
        cursor.execute("SELECT number, name, username, user_id, city, phone FROM list_1 WHERE number>=?",
                       [(number1)])
    else:
        cursor.execute("SELECT number, name, username, user_id, city, phone FROM list_1 WHERE number>=? AND number<=?",
                   [(number1), (number2)])
    res = cursor.fetchall()
    for i in res:
        a = str(i)
        bot.send_message(message.from_user.id, a[1:-1])
    conn.close()

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, f"Из какого ты города, {message.text}?")
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    global city
    city = message.text
    bot.send_message(message.from_user.id, "Твой номер телефона?")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    global phone
    phone = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_tel = types.InlineKeyboardButton(text='telegram', callback_data='tel')
    key_viber = types.InlineKeyboardButton(text='viber', callback_data='viber')
    key_wat = types.InlineKeyboardButton(text='watsapp', callback_data='wat')
    keyboard.add(key_tel, key_viber, key_wat)
    question = 'Какой тип связи тебе удобнее?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "swap":
        keyboard = types.InlineKeyboardMarkup()
        key_swap1 = types.InlineKeyboardButton(text='Далее', callback_data='swap1')
        keyboard.add(key_swap1)
        bot.send_message(call.message.chat.id, text="Если хочешь подробно узнать, как ты сможешь зарабатывать, "
                                                "и пройти 2-х дневное. вводное в профессию, бесплатное, онлайн-обучение"
                                                " (Без оплаты), тогда регистрируйся и приступай в кратчайшие сроки к"
                                                " обучению!"
                         , reply_markup=keyboard)
    elif call.data == "swap1":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("📋 Регистрация")
        item2 = types.KeyboardButton("😎 Для админа")
        markup.add(item1, item2)
        bot.send_message(call.message.chat.id, 'Молодец! Жми кнопку "Регистрация"⬇️', reply_markup=markup)
    elif call.data == "tel" or call.data == "viber" or call.data == "wat":
        connection = str(call.data)
        bot.send_message(call.message.chat.id, 'Ты зарегистрирован! Жди от меня известий!🖐')
        telegramm_base(connection)

bot.polling(none_stop=True, interval=0)