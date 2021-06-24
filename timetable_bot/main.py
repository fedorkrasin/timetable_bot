from telebot import types
import re
import sqlite3
from enum import Enum
from peewee import *
from sqlite3 import Error
import telebot

TOKEN = '1862242913:AAGCLBCJ2-XH8bFHmZ_8EbPGaQWSe8ITlpI'
bot = telebot.TeleBot(TOKEN)

days = ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
time = ["08:15–09:35", "09:45–11:05", "11:15-12:35", "13:00-14:20", "14:30-15:50", "16:00-17:20"]


# Подключение БД
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# Извлечение данных из БД
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# Helper
@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id, 'Данный бот несёт в себе информацию о расписании занятий '
                                      'Механико-математического факультета БГУ')


# Get timetable
@bot.message_handler(commands=['timetable'])
def get_course(message):
    bot.send_message(message.chat.id, "Введите ваш курс, группу и день недели в формате \"курс_группа\" ("
                                      "например 2_9): ")


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()
    if 3 <= len(get_message_bot) <= 4:
        global g
        g = get_message_bot
        bot.send_message(message.chat.id, "Введите номер дня недели: ")
    if get_message_bot == "1":
        res = get_day(1, g)
        bot.send_message(message.chat.id, res)
    if get_message_bot == "2":
        res = get_day(2, g)
        bot.send_message(message.chat.id, res)
    if get_message_bot == "3":
        res = get_day(3, g)
        bot.send_message(message.chat.id, res)
    if get_message_bot == "4":
        res = get_day(4, g)
        bot.send_message(message.chat.id, res)
    if get_message_bot == "5":
        res = get_day(5, g)
        bot.send_message(message.chat.id, res)
    if get_message_bot == "6":
        res = get_day(6, g)
        bot.send_message(message.chat.id, res)


def get_day(day, group_id):
    cursor.execute("SELECT * FROM Timetable WHERE day = ? and group_id = ?", (day, group_id))
    timetable = cursor.fetchall()
    course = group_id[0]
    group = group_id[2:]
    print("Расписание занятий " + group + " группы " + course + " курса на " + days[day] + ": ")
    res = "🕓 Расписание занятий " + group + " группы " + course + " курса на " + days[day] + ": \n\n"

    for i in range(len(timetable)):
        cursor.execute("SELECT name from Subjects WHERE id = " + str(timetable[i][2]))
        subject = str(cursor.fetchall()[0][0])

        if (len(str(timetable[i][1]))) > 0:
            cursor.execute("SELECT name from Teachers WHERE id = " + str(timetable[i][1]))
            teacher = str(cursor.fetchall()[0][0])
            teacher = ", " + teacher
        else:
            teacher = ''

        if (len(str(timetable[i][6]))) > 0:
            audience = "ауд. " + str(timetable[i][6])
        else:
            audience = 'дистанционно'

        if day == 3:
            tt = ''
        else:
            tt = time[timetable[i][4] - 1] + ": "

        print(tt + subject + teacher + ", " + audience)
        res += "▪️" + tt + subject + teacher + ", " + audience + "\n"

    return res


# Run Bot
connection = create_connection("timetable.db")

conn = SqliteDatabase("timetable.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Timetable WHERE day = 1 and group_id = '2_9'")
results = cursor.fetchall()
bot.polling(none_stop=True)

conn.close()
