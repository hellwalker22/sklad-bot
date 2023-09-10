import telebot                                              # импортируем библиотеку pytelegrambotapi
from telebot import types                                   # для указание типов
from datetime import date                                   # импортируем библиотеку текущего времени

TOKEN = "6562200271:AAHy2JORpEQriYgM1xh4kl4GWSNn3gdWKBk"    # токен моего бота
bot = telebot.TeleBot(TOKEN)                                # передаём токен боту

def task(number):                                                    # --функция расстановки точек в числе---
    number = str(number)[::-1]
    result = ''
    for i, num in enumerate(number):
        if i % 3 == 0:
            result += '.'
        result += num
    result = result[::-1][:-1]
    return result

def write_txt(total_many, day_many):                                      # ---функция записи суммы в .txt файл---
    current_date = date.today()                             # записываем в переменную текущую дату
    file2 = open('summa_s_date.txt', 'a')                   # открываем файл для записи
    file2.write(str(current_date)+""+str(":")+" "+str(task(day_many))+"\n")    # записываем в файл значение переменной
    file2.close()                                           # закрываем файл
    file = open('summa_zayavok.txt', 'w')                   # открываем файл для записи
    file.write(str(total_many))                             # записываем в файл значение переменной
    file.close()                                            # закрываем файл

@bot.message_handler(commands=['start'])                    # обрабатывает от бота команду /start
def start(message):                                             # ---функция самого бота---
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Список дней")                  # кнопка 1
    markup.add(btn1)                                            # добавляем кнопки
    bot.send_message(message.chat.id,                           # приветственное сообщение
                     text="Привет, {0.first_name}! Я бот для учета твоих заявок".format(
                         message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])                # обрабатывает от бота только text
def get_text_messages(message):                                     # ---функция самого бота---
    file = open('summa_zayavok.txt', 'r')                   # открываем файл для чтения
    total_many = file.read()                                # читаем файл
    print("Текст пользователя:", message.text)              # печатаем в консоль, что ввел пользователь
    if message.text == "/clear":                            # если ввели эту команду очищаем файл
        bot.send_message(message.from_user.id, "Сумма заявок и даты очищены")  # бот пишет в чат
        print("Пользователь очистил сумму")                 # печатаем в консоль
        file2 = open('summa_s_date.txt', 'w')               # открываем файл для записи
        file2.write("")                                     # записываем в файл пустоту
        file2.close()                                       # закрываем файл
        file = open('summa_zayavok.txt', 'w')               # открываем файл для записи
        file.write('0')                                     # записываем в файл 0
        file.close()                                        # закрываем файл
    elif message.text == "Список дней":                     # если нажали кнопку Список дней
        file2 = open('summa_s_date.txt', 'r')               # открываем файл для чтения
        total_days = file2.readlines()                      # читаем все строчки из файла
        file2.close()                                       # закрываем файл
        for i in total_days:                                # цикл перебора всех строчек
            bot.send_message(message.from_user.id, i)       # бот пишет в чат
    else:                                                   # иначе без команды
        try:                                                         # ---функция детекта ошибок---
            day_many = message.text                           # присваиваем переменной текст пользователя
            total_many = int(day_many) + int(total_many)      # складываем введённое число и всю сумму
            write_txt(total_many, day_many)                             # вызываем функцию с передачей суммы
            procent_many = (total_many / 100) * 1             # получаем процент от суммы
            print("Сумма всех введёных заявок:", task(total_many))  # печатаем в консоль
            print("1% прибыли с заявок:",  task(int(procent_many)))       # печатаем в консоль
            summa = "Сумма всех введёных заявок: \n" +str(task(total_many))  # сбор сообщения в переменную
            procent = "1% прибыли с заявок: \n" +str(task(int(procent_many)))  # сбор сообщения в переменную
            bot.send_message(message.from_user.id, summa)                 # бот пишет в чат
            bot.send_message(message.from_user.id, procent)               # бот пишет в чат
        except ValueError:                                                # ---детект ошибки---
            bot.send_message(message.from_user.id,
                             "Данные не приняты. Используйте только числа, без точек, запятых и пробелов!!!")  # бот пишет в чат
            print("Пользователь ввёл строковый тип данных")  # печатаем в консоль
bot.polling(none_stop=True, interval=0)  # конец кода
