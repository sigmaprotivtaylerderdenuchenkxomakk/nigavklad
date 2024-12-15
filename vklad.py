import sqlite3
from telebot import *
Token = '7955185006:AAGUu8tpE0MX9RrkVhqycnaD9Iap-Dm1ru0'
bot = TeleBot(Token)
@bot.message_handler(commands=['start'])
def handle_start(message):
    k = types.InlineKeyboardMarkup()
    j = types.InlineKeyboardButton('да', callback_data='0')
    l = types.InlineKeyboardButton('нет', callback_data='1')
    k.add(j)
    k.add(l)




    bot.send_message(message.chat.id,'Вы пользовались нашей программой ранее',reply_markup=k)
    con = sqlite3.connect('vklad.db')
    sql = con.execute ("""
        CREATE TABLE IF NOT EXISTS vk(
        
        id INTEGER PRIMARY KEY,
        sum REAL,
        proc REAL,
        plus REAL,
        hola REAL,
        chat INTEGER
        
        )


    """)
def textic(message):
    
    con = sqlite3.connect('vklad.db')
    text = message.text
    if text.isdigit():
        bot.send_message(message.chat.id,'Процент вклада(только число)')
        bot.register_next_step_handler(message,textik)
        k =con.execute     ("""
        INSERT INTO vk (sum, chat) 
        VALUES(?,?)

    """,[text, message.chat.id])
    else:
        bot.send_message(message.chat.id,'Введите сумму вклада') 
        bot.send_message(message.chat.id,'ИЗ ЦИФР') 
        bot.register_next_step_handler(message, textic)
    con.commit()
def textik(message):
    con = sqlite3.connect('vklad.db')
    textt = message.text
    if textt.isdigit():
        bot.send_message(message.chat.id,'красава')
        og = con.execute(f"""
    SELECT sum FROM vk WHERE chat = {message.chat.id}


""").fetchall()
        c = og[0][0]*int(textt)/100/12
        k =con.execute     (f"""
        UPDATE vk 
        SET proc = {textt},
        plus = {c},
        hola = {c+og[0][0]}
        WHERE chat = {message.chat.id}

    """)
        con.commit()
        
    else:
        bot.send_message(message.chat.id,'Процент вклада ') 
        bot.send_message(message.chat.id,'ИЗ ЦИФР') 
        bot.register_next_step_handler(message, textik)
    
def textis(message):
    con = sqlite3.connect('vklad.db')
    texttt = message.text
    if texttt.isdigit():
        bot.send_message(message.chat.id,'красава')
        texttt = int(texttt)
        kjh = con.execute("""
            SELECT hola FROM vk
""").fetchall()[-1][0]
        k =con.execute     ("""
        INSERT INTO vk (sum,proc,plus,hola,chat) 
        VALUES(?,?,?,?,?)
    """,[kjh,texttt,texttt/100/12*kjh,kjh+texttt/100/12*kjh,message.chat.id])
        con.commit()

@bot.callback_query_handler(func=lambda callback:True)
def handle_callback(callback):
    if callback.data == '1':

        bot.send_message(callback.message.chat.id,'Введите сумму вклада')
        bot.register_next_step_handler(callback.message,textic)
    else:
        bot.send_message(callback.message.chat.id,'Процент вклада(только число)')
        bot.register_next_step_handler(callback.message,textis)

        


bot.polling(non_stop=True,interval=1)