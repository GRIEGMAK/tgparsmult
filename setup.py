#!/bin/env python3

"""

you can re run setup.py 
if you have added some wrong value

"""
re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

import csv
import os
import sys
import time


def banner():
	os.system('clear')
	print(f"""
	{re}╔═╗{cy}┌─┐┌┬┐┬ ┬┌─┐
	{re}╚═╗{cy}├┤  │ │ │├─┘
	{re}╚═╝{cy}└─┘ ┴ └─┘┴
	""")

def requirements():
	def csv_lib():
		banner()
		print(gr+'['+cy+'+'+gr+']'+cy+' this may take some time ...')
		os.system("""
			pip3 install cython numpy pandas python-socks
			python3 -m pip install cython numpy pandas python-socks 
			""")
	banner()
	print(gr+'['+cy+'+'+gr+']'+cy+' it will take upto 10 min to install csv merge.')
	input_csv = input(gr+'['+cy+'+'+gr+']'+cy+' do you want to enable csv merge (y/n): ').lower()
	if input_csv == "y":
		csv_lib()
	else:
		pass
	print(gr+"[+] Installing requierments ...")
	os.system("""
		pip3 install telethon requests configparser
		python3 -m pip install telethon requests configparser
		touch config.data
		""")
	banner()
	print(gr+"[+] requierments Installed.\n")

def change_invite_count():
	import configparser
	banner()
	phone = input('Введите номер: ')
	csv_accounts = csv.reader(open('accounts.csv', "r"), delimiter=",")
	g = 0
	for cpass in csv_accounts:
		if phone == cpass[2]:
			invite_count = cpass[3]
			g = 1
		if g == 0:
			print('Данный аккаунт в базе найти не удалось ')
			g = input("Нажмите enter затем внесите номер в базу и перезапустите скрипт:")
			sys.exit(1)
	print("Сейчас количество инвайтов на данном аккаунте:", invite_count)
	print("""	Значение которое вы введете не должно превышать 50 
	а так же не должно содержать иных символов кроме числа
	если быть точнее 1-50""")
	xinvite = int(input('Введите число инвайтов на номер ' + phone + ': '))
	if xinvite is None or xinvite > 50:
		sys.exit('Перезапустите программу потому как значение вы ввели не корректное')
	r = csv.reader(open('accounts.csv'))
	lines = list(r)
	for line in lines:
		if phone == line[2]:
			line[3] = xinvite
	writer = csv.writer(open('accounts.csv', 'w'))
	writer.writerows(lines)

def config_setup():
	import configparser
	banner()
	file_name = "accounts.csv"
	accounts = int(input("Сколько аккаунтов планируется добавить? Введите числом:"))
	if os.path.exists(file_name):
		print('Данные будут записаны в файл ' + file_name)
	else:
		f = open(file_name, "w")
		f.close()
	with open(file_name,"a",encoding='UTF-8') as f:
		cpass = csv.writer(f,delimiter=",",lineterminator="\n")
		for i in range(accounts):
			xid = input(gr+"[+] enter api ID: "+re)
			xhash = input(gr+"[+] enter hash ID: "+re)
			xphone = input(gr+"[+] enter phone number: "+re)
			xinvite = input(gr+"[+] enter invite count: "+re)
			if(xinvite == "" or not xinvite.isdigit()):
				xinvite = 50
			print(gr+"[+] setup complete !")
			cpass.writerow([xid, xhash, xphone, xinvite])

def add_proxy():
	file_name = "proxy.csv"
	count_proxy = int(input("Сколько прокси планируется добавить?"))
	if os.path.exists(file_name):
		print('Данные будут записаны в файл ' + file_name)
	else:
		f = open(file_name, "w")
		f.close()
	with open(file_name,"a",encoding='UTF-8') as f:
		cpassproxy = csv.writer(f,delimiter=",",lineterminator="\n")
		for i in range(count_proxy):
			xproxy_serv = input("Введите значение ip прокси сервера")
			xproxy_port = input("Введите значение порта у прокси сервера")
			xproxy_key = input("Введите логин")
			xproxy_pass = input("Введите пароль")
			xproxy_type = int(input("Выберите тип подключения 1 - http; 2 - socks5"))
			cpassproxy.writerow([xproxy_type, xproxy_serv, xproxy_port, xproxy_key, xproxy_pass])

def merge_csv():
	import sys

	import pandas as pd
	banner()
	file1 = pd.read_csv(sys.argv[2])
	file2 = pd.read_csv(sys.argv[3])
	print(gr+'['+cy+'+'+gr+']'+cy+' merging '+sys.argv[2]+' & '+sys.argv[3]+' ...')
	print(gr+'['+cy+'+'+gr+']'+cy+' big files can take some time ... ')
	merge = file1.merge(file2, on='username')
	merge.to_csv("output.csv", index=False)
	print(gr+'['+cy+'+'+gr+']'+cy+' saved file as "output.csv"\n')

def update_tool():
	import requests as r
	banner()
	source = r.get("https://raw.githubusercontent.com/th3unkn0n/TeleGram-Scraper/master/.image/.version")
	if source.text == '3':
		print(gr+'['+cy+'+'+gr+']'+cy+' alredy latest version')
	else:
		print(gr+'['+cy+'+'+gr+']'+cy+' removing old files ...')
		os.system('rm *.py');time.sleep(3)
		print(gr+'['+cy+'+'+gr+']'+cy+' getting latest files ...')
		os.system("""
			curl -s -O https://raw.githubusercontent.com/th3unkn0n/TeleGram-Scraper/master/add2group.py
			curl -s -O https://raw.githubusercontent.com/th3unkn0n/TeleGram-Scraper/master/scraper.py
			curl -s -O https://raw.githubusercontent.com/th3unkn0n/TeleGram-Scraper/master/setup.py
			curl -s -O https://raw.githubusercontent.com/th3unkn0n/TeleGram-Scraper/master/smsbot.py
			chmod 777 *.py
			""");time.sleep(3)
		print(gr+'\n['+cy+'+'+gr+']'+cy+' update compled.\n')

try:
	if any ([sys.argv[1] == '--config', sys.argv[1] == '-c']):
		print(gr+'['+cy+'+'+gr+']'+cy+' selected module : '+re+sys.argv[1])
		config_setup()
	elif any ([sys.argv[1] == "--changeinvite", sys.argv[1] == '-cic']):
		change_invite_count()
	elif any ([sys.argv[1] == "--addproxy", sys.argv[1] == '-ap']):
		add_proxy()
	elif any ([sys.argv[1] == '--merge', sys.argv[1] == '-m']):
		print(gr+'['+cy+'+'+gr+']'+cy+' selected module : '+re+sys.argv[1])
		merge_csv()
	elif any ([sys.argv[1] == '--update', sys.argv[1] == '-u']):
		print(gr+'['+cy+'+'+gr+']'+cy+' selected module : '+re+sys.argv[1])
		update_tool()
	elif any ([sys.argv[1] == '--install', sys.argv[1] == '-i']):
		requirements()
	elif any ([sys.argv[1] == '--help', sys.argv[1] == '-h']):
		banner()
		print("""$ python3 setup.py -m file1.csv file2.csv
			
	( --config  / -c ) setup api configration
	( --changeinvite / -cic ) изменения количества инвайтов на аккаунт
	( --addproxy / -ap ) добавление прокси
	( --merge   / -m ) merge 2 .csv files in one 
	( --update  / -u ) update tool to latest version
	( --install / -i ) install requirements
	( --help    / -h ) show this msg 
			""")
	else:
		print('\n'+gr+'['+re+'!'+gr+']'+cy+' unknown argument : '+ sys.argv[1])
		print(gr+'['+re+'!'+gr+']'+cy+' for help use : ')
		print(gr+'$ python3 setup.py -h'+'\n')
except IndexError:
	print('\n'+gr+'['+re+'!'+gr+']'+cy+' no argument given : '+ sys.argv[1])
	print(gr+'['+re+'!'+gr+']'+cy+' for help use : ')
	print(gr+'['+re+'!'+gr+']'+cy+' https://github.com/th3unkn0n/TeleGram-Scraper#-how-to-install-and-use')
	print(gr+'$ python3 setup.py -h'+'\n')
