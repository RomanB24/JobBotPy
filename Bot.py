import time
import telebot
from telebot import types
import psycopg2
from postgresqlclass import PostgresqlDBManagementSystem
import pandas as pd
import csv

db = PostgresqlDBManagementSystem(host= '', user='', password='', database='')

bot = telebot.TeleBot('')

name = ''
surname = ''
age = 0
number = ''
exp = ''
prog = ''
education = ''
vacant = ''
vac_select = ''

@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(content_types=['text', 'document'])

def send_welcome(message):
	bot.send_message(message.from_user.id,
					 'Здравствуйте, это бот компании ООО "Компания", для найма персонала. Если вы кандидат нажмите /reg. Для просмотра кандидатов HR нажмите /adm');
	bot.register_next_step_handler(message, func);

def func(message):
	if message.text == '/adm':
		bot.send_message(message.from_user.id, "Введите УЗ Админа/HR");
		bot.register_next_step_handler(message, admin_func);
	if message.text == '/reg':
		bot.send_message(message.from_user.id, "Как Вас зовут?");
		bot.register_next_step_handler(message, get_name);

def admin_func(message):
	if message.text == '':
		keyboard = types.InlineKeyboardMarkup()
		key_updatedat = types.InlineKeyboardButton(text='Обновить данные', callback_data='updatedat')
		keyboard.add(key_updatedat)
		question = 'Нажмите на нужную функцию.'
		bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
	else:
		bot.send_message(message.from_user.id, "У вас нет достпука к данному функционалу, для соискателей нажмите /reg");

def sel_vac():
	vac = db.select_all('users')
	candidate = []
	for it in vac:
		it2 = it[1:]
		candidate.append(it2)
	with open("candit.csv", mode="w", encoding='utf-8') as w_file:
		file_writer = csv.writer(w_file, delimiter=',')
		for can in candidate:
			file_writer.writerow(can)
	df = pd.read_csv("candit.csv", delimiter=',',
					 names=['Имя', 'Фамилия', 'Возраст', 'Тел', 'Опыт', 'Программы', 'Образование', 'Вакансия'])
	frame = pd.DataFrame(df)
	frame.set_index('Вакансия', inplace=True)
	frame.to_csv("Kandidats.csv", encoding="cp1251", sep=',')

def get_name(message):
	global name
	name = message.text
	bot.send_message(message.from_user.id, 'Какая у Вас Фамилия?')
	bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Напишите ваш номер телефона для связи!')
    bot.register_next_step_handler(message, get_number)

def get_number(message):
	global number
	number = message.text
	bot.send_message(message.from_user.id, 'Укажите ваш опыт работы в желаемой вакансии. Количество полных лет.')
	bot.register_next_step_handler(message, get_exp)

def get_exp(message):
	global exp
	exp = message.text
	bot.send_message(message.from_user.id, 'Перечислите с какими программами работали')
	bot.register_next_step_handler(message, get_prog)

def get_prog(message):
	global prog
	prog = message.text
	bot.send_message(message.from_user.id, 'Укажите уровень образования, так же если проходили курсы можете их указать')
	bot.register_next_step_handler(message, get_education)

def get_education(message):
	global education
	education = message.text
	bot.send_message(message.from_user.id, 'Сколько Вам лет, укажите цифрами.')
	bot.register_next_step_handler(message, get_age)

def get_age(message):
	global age
	try:
		age = int(message.text)
	except Exception:
		bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
	bot.send_message(message.from_user.id, 'Прикрепите файл с резюме, либо напишите нет.')
	bot.register_next_step_handler(message, get_file)

def get_file(message):
	if message.text == 'Нет' or message.text == 'нет':
		bot.send_message(message.from_user.id, 'Вы отказались прикрепить резюме.')
		keyboard = types.InlineKeyboardMarkup()
		key_buh = types.InlineKeyboardButton(text='Бухгалтер', callback_data='buh')
		keyboard.add(key_buh)
		key_kassir = types.InlineKeyboardButton(text='Кассир', callback_data='kassir')
		keyboard.add(key_kassir)
		key_tovaroved = types.InlineKeyboardButton(text='Товаровед', callback_data='tovaroved')
		keyboard.add(key_tovaroved)
		question = 'Выберите желаемую вакансию:'
		bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		key_buh = types.InlineKeyboardButton(text='Бухгалтер', callback_data='buh')
		keyboard.add(key_buh)
		key_kassir = types.InlineKeyboardButton(text='Кассир', callback_data='kassir')
		keyboard.add(key_kassir)
		key_tovaroved = types.InlineKeyboardButton(text='Товаровед', callback_data='tovaroved')
		keyboard.add(key_tovaroved)
		question = 'Выберите желаемую вакансию:'
		bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)




@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	global name
	global surname
	global age
	global number
	global exp
	global prog
	global education
	global vacant
	if call.data == "buh":
		bot.send_message(call.message.chat.id, 'Вы выбрали вакансию Бухгалтер. Наш сотрудник свяжется с вами.')
		vacant = 'Бухгалтер'
		try:
			db.insert('users (name,surname,age,number,exp,prog,education,vacant)', name, surname, age, number, exp, prog, education, vacant)
		except Exception:
			print('Не удалось записать БД')

	elif call.data == "kassir":
		bot.send_message(call.message.chat.id, 'Вы выбрали вакансию Кассира. Наш сотрудник свяжется с вами.')
		vacant = 'Кассир'
		try:
			db.insert('users (name,surname,age,number,exp,prog,education,vacant)', name, surname, age, number, exp, prog, education, vacant)
		except Exception:
			print('Не удалось записать БД')
	elif call.data == "tovaroved":
		bot.send_message(call.message.chat.id, 'Вы выбрали вакансию Товаровед. Наш сотрудник свяжется с вами.')
		vacant = 'Товаровед'
		try:
			db.insert('users (name,surname,age,number,exp,prog,education,vacant)', name, surname, age, number, exp,
					  prog, education, vacant)
		except Exception:
			print('Не удалось записать БД')
	elif call.data == 'updatedat':
		try:
			sel_vac()
			bot.send_message(call.message.chat.id, 'Данные обновлены, посмотрите на сайте: http://127.0.0.1:8050/')
		except Exception as e:
			bot.send_message(call.message.chat.id, 'Ошибка обновления данных')

bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
	bot.polling(none_stop=True, interval=0)
