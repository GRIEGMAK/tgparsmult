from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import Channel, InputPeerEmpty
import os, sys
import configparser
import csv
import time
import socks

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
    if(csv_accounts == []):
        proxy_number = int(input("Введите номер прокси которой будет использоваться, Если вы не хотите использовать прокси введите 0 "))
    else:
        proxy_number = 0
    if proxy_number != 0:
        for cpass in csv_accounts:
            if numbering == proxy_number:
                proxy_type = cpass[0]
                proxy_ip = cpass[1]
                proxy_port = cpass[2]
                proxy_login = cpass[3]
                proxy_pass = cpass[4]
            numbering += 1
            g = 1
        if g == 0:
            print("Прокси нет, подключаемся без них")
            client = TelegramClient(phone, api_id, api_hash)
        else:
            if proxy_type == 1:
                proxy = (socks.SOCKS5, proxy_ip, proxy_port, proxy_login, proxy_pass)
            else:
                proxy = (socks.SOCKS5, proxy_ip, proxy_port, proxy_login, proxy_pass)
            client = TelegramClient(phone, api_id, api_hash ,proxy=proxy)
    else:
        client = TelegramClient(phone, api_id, api_hash)
    return client

def parser(number, file_name):
    import os
    try:
        csv_accounts = csv.reader(open('accounts.csv', "r"), delimiter=",")
        g = 0
        for cpass in csv_accounts:
            if number == cpass[2]:
                api_id = cpass[0]
                api_hash = cpass[1]
                phone = cpass[2]
                g = 1
        if g == 0:
            print('Данный аккаунт в базе найти не удалось ')
            g = input("Нажмите enter затем внесите номер в базу и перезапустите скрипт:")
            sys.exit(1)
        client = connectionTelegramAccount(phone, api_id, api_hash)
        
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
        client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
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
    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue
 
    print(gr+'[+] Choose a group to scrape members :'+re)
    i=0
    for g in groups:
        print(gr+'['+cy+str(i)+gr+']'+cy+' - '+ g.title)
        i+=1
 
    print('')
    g_index = input(gr+"[+] Enter a Number : "+re)
    target_group=groups[int(g_index)]
 
    print(gr+'[+] Fetching Members...')
    time.sleep(1)
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)
 
    print(gr+'[+] Saving In file...')
    time.sleep(1)
    import os.path
    if os.path.exists(file_name):
        print('Данные будут записаны в файл' + file_name)
    else:
        f = open(file_name, "w")
        f.close()
    with open(file_name,"a",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        for user in all_participants:
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
    print(gr+'[+] Members scraped successfully.')


number = sys.argv[1]
parser(number, "members.csv")