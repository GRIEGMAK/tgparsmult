#!/usr/bin/env python3
from telethon import client
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random
from telethon import connection

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

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

def inviter(file_name, target_group_id, start_value, api_id, api_hash, phone, invite_count, mode):
    import time, os
    finished = 0
    try:
        client = connectionTelegramAccount(phone, api_id, api_hash)
    except KeyError:
        os.system('clear')
        banner()
        print(re+"[!] run python3 setup.py first !!\n")
        sys.exit(1)
    if client.is_connected() == False:
        client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        os.system('clear')
        banner()
        client.sign_in(phone, input(gr+'[+] Enter the code на аккаунте '+ phone +': '+re))
    os.system('clear')
    banner()
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash = 0
    ))
    chats.extend(result.chats)
    n = 0
    for chat in chats:
        try:
            if chat.megagroup== True:
                groups.append(chat)
        except:
            continue

    i = 0
    for group in groups:
        if group.id == target_group_id:
            target_group = group
        i += 1
    if target_group is None:
        return 0

    print('Start with:', start_value)
    count_user = 0
    users = []
    with open(file_name,"r",encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        for row in rows:
            if count_user >= start_value + int(invite_count):
                break
            if count_user >= start_value:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
                if user == []:
                    finished = 1
            count_user +=1

    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

    print('before for') 
    for user in users:
        time.sleep(1)
        if user is None and finished == 1:
            sys.exit(1)
        try:
            print ("Adding {}".format(user['id']))
            if mode == 2:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 1:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit(re+"[!] Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity,[user_to_add]))
            start_value += 1
            print(gr+"[+] Waiting for 10-30 Seconds...")
            time.sleep(random.randrange(10, 30))
            temp = configparser.RawConfigParser()
            temp.read('config.data')
            temp.set('START_value', 'invite', start_value)
            with open('config.data', "w") as config_file:
                temp.write(config_file)
            print(start_value)
        except PeerFloodError:
            print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
        except UserPrivacyRestrictedError:
            print(re+"[!] The user's privacy settings do not allow you to do this. Skipping.")
        except:
            traceback.print_exc()
            print(re+"[!] Unexpected Error")
            continue
    client.log_out()
    client.disconnect()
    import os
    files= next(os.walk(r'./'))[2]
    for filename in files:
        ex=filename.split(".")[-1]
        if ex=='session':
            os.unlink(filename)

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
client = TelegramClient(phone, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code на аккаунте '+ phone +': '+re))

chats = []
last_date = None
chunk_size = 200
groups=[]
result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash = 0
))
chats.extend(result.chats)
n = 0
for chat in chats:
    try:
        if chat == True:
            groups.append(chat)
    except:
        continue

i=0
for group in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+group.title)
    i+=1

print(gr+'[+] Choose a group to add members')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group=groups[int(g_index)]
target_group_id = target_group.id
client.log_out()
client.disconnect()
import os
import shutil
files= next(os.walk(r'./'))[2]
for filename in files:
    ex=filename.split(".")[-1]
    if ex=='session':
       os.remove(filename)

print(gr+"[1] add member by user ID\n[2] add member by username ")
mode = int(input(gr+"Input : "+re)) 
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
    inviter(input_file, target_group_id, start_value, api_id, api_hash, phone, invite_count, mode)