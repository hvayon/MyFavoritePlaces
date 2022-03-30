import telebot;
from telebot import types
bot = telebot.TeleBot('5283823915:AAEVgR1gyv7LyKkYH99G90_SMjIUMbXOQCw');
name = ''
info = []
current_info = [0, '', '', 0, 0]
import sqlite3
connection = sqlite3.connect('shows.db', check_same_thread=False)
cursor = connection.cursor()

@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler(commands=['help'])
def get_text_messages(message):
    bot.send_message(message.chat.id, '/help - view help\n/start - start work\n/add - add new place')

@bot.message_handler(commands=['add'])
def get_text_messeges(message):
    current_info[0] = message.from_user.id
    bot.send_message(message.from_user.id, "Введите название места")
    bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name

def get_name(message):
    global name
    current_info[1]=(message.text)
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Хочешь ли ты добавить фото?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Пришлите фото')
        bot.register_next_step_handler(call.message, get_photo)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Пришлите геолокацию')
        bot.register_next_step_handler(call.message, get_geo)

#@bot.message_handler(content_types=["photo"])
def get_photo(message):
   current_info[2]=(message.photo[0].file_id)
   #bot.send_photo(message.chat.id, idphoto)
   bot.send_message(message.chat.id, 'Пришлите геолокацию')
   bot.register_next_step_handler(message, get_geo)

def get_geo(message):
    current_info[3]=(message.location.latitude)
    current_info[4]=(message.location.longitude)
   # info.extend(current_info)


    sqlite_insert_with_param = """INSERT INTO Places (ChatID, Name, Image, latitude, longitude)
VALUES (?, ?, ?, ?, ?);"""

    data_tuple = (current_info[0], current_info[1], current_info[2], current_info[3], current_info[4])
    cursor.execute(sqlite_insert_with_param, data_tuple)
    connection.commit()

    bot.send_message(message.chat.id, 'Все сохранено')

@bot.message_handler(commands=['list'])
def get_text_messeges(message):
    sqlite_insert_with_param = '''select * from Places where ChatID=?'''
    data_tuple = (message.chat.id,)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    records = cursor.fetchall()
    for i in records:
        text = "Координаты " + str(i[3]) + ' ' + str(i[4]) + "Название - " + i[1]
        try:
            bot.send_photo(message.chat.id, i[2], caption=text)
        except:
            bot.send_message(message.chat.id, text)


# def get_photo(message):
#     print("2")
#     keyboard = types.InlineKeyboardMarkup() #наша клавиатура
#     key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
#     keyboard.add(key_yes); #добавляем кнопку в клавиатуру
#     key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
#     keyboard.add(key_no);
#     question = 'Хочешь ли ты добавить фото?';
#     bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)