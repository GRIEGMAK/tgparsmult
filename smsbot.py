#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import configparser
import os, sys
import csv
import random
import time
from telethon import connection

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
SLEEP_TIME = 30

class main():

    def banner():
        
        print(f"""
    {re}╔╦╗{cy}┌─┐┌─┐┌─┐┌─┐┬─┐{re}╔═╗
    {re} ║ {cy}├─┐├┤ ├─┘├─┤├┬┘{re}╚═╗
    {re} ╩ {cy}└─┘└─┘┴  ┴ ┴┴└─{re}╚═╝
    by https://github.com/elizhabs
            """)

    def connectionTelegramAccount(phone, api_id, api_hash):
        csv_accounts = csv.reader(open('proxy.csv', "r"), delimiter=",")
        g = 0
        numbering = 1
        i = 1
        file_name = 'proxy.csv'
        if not os.path.exists(file_name):
            f = open(file_name, "w")
            f.close()
        for cpass in csv_accounts:
            print (i, ")", cpass[0], cpass[1])
            i += 1
        proxy_number = int(input("Введите номер прокси которой будет использоваться, Если вы не хотите использовать прокси введите 0 "))
        if proxy_number != 0:
            for cpass in csv_accounts:
                if numbering == proxy_number:
                    proxy_server = cpass[0]
                    proxy_port = cpass[1]
                    proxy_key = cpass[2]
                numbering += 1
                g = 1
            if g == 0:
                print("Прокси нет, подключаемся без них")
                client = TelegramClient(phone, api_id, api_hash)
            else:
                proxy = (proxy_server, proxy_port, proxy_key)
                client = TelegramClient(phone, api_id, api_hash, connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,proxy=proxy)
        else:
            client = TelegramClient(phone, api_id, api_hash)
        return client


    def send_sms(g, file_name):
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            csv_accounts = csv.reader(open('accounts.csv', "r"), delimiter=",")
            for cpass in csv_accounts:
                api_id = cpass[0]
                api_hash = cpass[1]
                phone = cpass[2]
        except KeyError:
            os.system('clear')
            main.banner()
            print(re+"[!] run python3 setup.py first !!\n")
            sys.exit(1)

        client = main.connectionTelegramAccount(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
        
        os.system('clear')
        main.banner()
        users = []
        with open(file_name, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        print(gr+"[1] send sms by user ID\n[2] send sms by username ")
        mode = int(input(gr+"Input : "+re))
         
        message = input(gr+"[+] Enter Your Message : "+re)

        for user in users:
            if mode == 2:
                if user['username'] == "":
                    continue
                receiver = client.get_input_entity(user['username'])
            elif mode == 1:
                receiver = InputPeerUser(user['id'],user['access_hash'])
            else:
                print(re+"[!] Invalid Mode. Exiting.")
                client.disconnect()
                sys.exit()
            try:
                print(gr+"[+] Sending Message to:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(1)
            except PeerFloodError:
                print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re+"[!] Error:", e)
                print(re+"[!] Trying to continue...")
                continue
        client.disconnect()
        print("Done. Message sent to all users.")

    def sms_multiaccount():
        cpass = configparser.RawConfigParser()
        cpass.read('config.data')
        for i in range(len(cpass)):
            main.send_sms(i, "members.csv")


main.sms_multiaccount()
