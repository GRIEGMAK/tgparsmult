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
        

def inviter(file_name, target_group, start_value, api_id, api_hash, phone):
    import time
    try:
        client = TelegramClient(phone, api_id, api_hash)
        print('ghbdt')
    except KeyError:
        os.system('clear')
        banner()
        print(re+"[!] run python3 setup.py first !!\n")
        sys.exit(1)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        os.system('clear')
        banner()
        client.sign_in(phone, input(gr+'[+] Enter the code на аккаунте '+ phone +': '+re))
    os.system('clear')
    banner()
    print("Привет")
    count_user = 0
    users = []
    with open(file_name,"r",encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
    for row in rows:
        if count_user >= start_value + 49:
            break
        if count_user >= start_value:
            user = {}
            user['username'] = row[0]
            user['id'] = row[1]
            user['access_hash'] = row[2]
            user['name'] = row[3]
            users.append(user)
            count_user += 1



    if target_group is None:
        target_group = addGroup(client)
    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
 
    print(gr+"[1] add member by user ID\n[2] add member by username ")
    mode = int(input(gr+"Input : "+re)) 
    n = 0
    print(users)
    print('before for') 
    for user in users:
        n += 1
        if 1 == 1:
            time.sleep(1)
            try:
                print ("Adding {}".format(user['id']))
                if mode == 1:
                    if user['username'] == "":
                        continue
                    user_to_add = client.get_input_entity(user['username'])
                elif mode == 2:
                    user_to_add = InputPeerUser(user['id'], user['access_hash'])
                else:
                    sys.exit(re+"[!] Invalid Mode Selected. Please Try Again.")
                client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                start_value = start_value + 1
                print(gr+"[+] Waiting for 10-30 Seconds...")
                time.sleep(random.randrange(10, 30))
                
            except PeerFloodError:
                print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
            except UserPrivacyRestrictedError:
                print(re+"[!] The user's privacy settings do not allow you to do this. Skipping.")
            except:
                traceback.print_exc()
                print(re+"[!] Unexpected Error")
                continue

def addGroup(client):
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

    for chat in chats:
        try:
            if chat.megagroup== True:
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
    return target_group


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
    break
first_client = TelegramClient(phone, api_id, api_hash)
target_group = addGroup(first_client)
for cpass in csv_accounts:
    api_id = cpass[0]
    api_hash = cpass[1]
    phone = cpass[2]
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
    inviter(input_file, target_group, start_value, api_id, api_hash, phone)
    temp.read('config.data')
    temp.set('START_value', 'invite', start_value)
