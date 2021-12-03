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
import python_socks

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
            """)

    def connectionTelegramAccount(phone, api_id, api_hash):
        file_name = 'proxy.csv'
        if not os.path.exists(file_name):
            f = open(file_name, "w")
            f.close()
        csv_accounts = csv.reader(open('proxy.csv', "r"), delimiter=",")
        g = 0
        numbering = 1
        i = 1
        for cpass in csv_accounts:
            print (i, ")", cpass[0], cpass[1])
            i += 1
        proxy_number = 0
        sys.stdout.write('\r\a')
        sys.stdout.flush()
        if(i > 1):
            proxy_number = input("Введите номер прокси которой будет использоваться, Если вы не хотите использовать прокси введите 0 ")
        if proxy_number != 0:
            csv_accounts = csv.reader(open('proxy.csv', "r"), delimiter=",")
            for cpass in csv_accounts:
                if numbering == int(proxy_number):
                    proxy_type = cpass[0]
                    proxy_ip = cpass[1]
                    proxy_port = cpass[2]
                    proxy_login = cpass[3]
                    proxy_pass = cpass[4]
                    g = 1
                    print(g)
                numbering += 1
            
            if g == 0:
                print()
                client = TelegramClient(phone, api_id, api_hash)
            else:
                print(int(proxy_type) == 2)
                if int(proxy_type) == 1:
                    proxy = {
                        'proxy_type': python_socks.ProxyType.HTTP,
                        'addr': proxy_ip,
                        'port': int(proxy_port), 
                        'username': proxy_login,      
                        'password': proxy_pass,      
                        'rdns': True            
                    }
                else:
                    proxy = {
                        'proxy_type': python_socks.ProxyType.SOCKS5,
                        'addr': proxy_ip,
                        'port': int(proxy_port),
                        'username': proxy_login,
                        'password': proxy_pass,
                        'rdns': True
                    }
                client = TelegramClient(phone, api_id, api_hash ,proxy=proxy)
        else:
            client = TelegramClient(phone, api_id, api_hash)
        return client


    def send_sms(message, api_id, api_hash, phone):

        client = main.connectionTelegramAccount(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
        
        os.system('clear')
        main.banner()
        input_file = sys.argv[1]
        users = []
        with open(input_file, encoding='UTF-8') as f:
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
    
    def sms_multiaccount(message):
        csv_accounts_file = open("accounts.csv","r+") 
        reader_file = csv.reader(csv_accounts_file) 
        value = len(list(reader_file)) 
        input_file = sys.argv[1]
        temp = configparser.RawConfigParser()
        csv_accounts = csv.reader(open('accounts.csv', "r"), delimiter=",")
        g = 0
        for row in csv_accounts:
            api_id = row[0]
            api_hash = row[1]
            phone = row[2]
            invite_count = row[3]
            break
        
        client = main.connectionTelegramAccount(phone, api_id, api_hash)
         
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
        
        csv_accounts = csv.reader(open('accounts.csv', "r"), delimiter=",")
        for cpass in csv_accounts:
            api_id = cpass[0]
            api_hash = cpass[1]
            phone = cpass[2]
            invite_count = cpass[3]
            temp = configparser.RawConfigParser()
            try:
                temp.read('config.data')
                start_value = int(temp.get('START_value', 'invite'))
            except:
                temp.add_section('START_value')
                temp.set('START_value', 'invite', 0)
                setup = open('config.data', 'w')
                temp.write(setup)
                setup.close()
                start_value = 0
            main.send_sms(message, api_id, api_hash, phone)
        
        


message = input(gr+"[+] Enter Your Message : "+re)
main.sms_multiaccount(message)
