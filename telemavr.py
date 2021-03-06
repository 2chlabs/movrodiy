#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @ru2chcc


import telepot
import requests
import threading
import time
import random
from telepot.loop import MessageLoop


banner = r"""
 __  __   ___ __     __ ____    ___   ____  ___ __   __
|  \/  | / _ \\ \   / /|  _ \  / _ \ |  _ \|_ _|\ \ / /
| |\/| || | | |\ \ / / | |_) || | | || | | || |  \ V /
| |  | || |_| | \ V /  |  _ < | |_| || |_| || |   | |
|_|  |_| \___/   \_/   |_| \_\ \___/ |____/|___|  |_|

"""


print(banner)
print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'Movrodiy initialized')

token = '' # token
ch_id = -1001383331161 # lock chat id, optional
quotes = ['ФИНАНСОВЫЙ АПОКАЛИПСИС НЕИЗБЕЖЕН', 'МЫ МОЖЕМ МНОГОЕ', 'МЫ МЕНЯЕМ МИР', 'РЕЖИМ СПОКОЙСТВИЕ', 'ВСЕМ ВСЕ ПЛАТИТСЯ', 'КУПЛЮ ЖЕНЕ САПОГИ', 'ВЫПЛАТЫ RIPPLE 2018 БУДУТ', 'ДА МНЕ ПОХУЙ ВООБЩЕ Я НА ЛУНЕ ЖИВУ', 'BUY MAVRO']
bot = telepot.Bot(token)


def price_update():
    global pdata
    global db

    while True:
        cldata = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
        pdata = cldata.json()

        db = {}
        for i in range(len(pdata) - 1):
            symbol_db = pdata[i]['symbol'].lower()
            id_db = i
            db.update({symbol_db: id_db})

        print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'DB updated: ' + str(len(db)))

        time.sleep(80)

def price_get(ch):
    name = pdata[ch]['name']
    symbol = pdata[ch]['symbol']
    rank = pdata[ch]['rank']
    price_usd = pdata[ch]['price_usd']
    price_btc = pdata[ch]['price_btc']
    volume_usd = pdata[ch]['24h_volume_usd']
    market_cap_usd = pdata[ch]['market_cap_usd']
    available_supply = pdata[ch]['available_supply']
    total_supply = pdata[ch]['total_supply']
    max_supply = pdata[ch]['max_supply']
    percent_change_1h = pdata[ch]['percent_change_1h']
    percent_change_24h = pdata[ch]['percent_change_24h']
    percent_change_7d = pdata[ch]['percent_change_7d']
    last_updated = pdata[ch]['last_updated']

    return name, symbol, rank, price_usd, price_btc, volume_usd, market_cap_usd, available_supply, total_supply, max_supply, percent_change_1h, percent_change_24h, percent_change_7d, last_updated

def commas(n):
    digits = str(n)
    assert(digits.isdigit())
    res = ''
    while digits:
        digits, last3 = digits[:-3], digits[-3:]
        if res:
            res = (last3 + ',' + res)
        else:
            res = last3
    return res

def handle(msg):
    if 'text' in msg:
        chat_id = msg['chat']['id']
        command = msg['text']

        if command[0] == '/' and chat_id == ch_id: # lock for one chat
            print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] ' + 'Got command: %s' % command)

            if command == '/help':
                bot.sendMessage(chat_id, 'Usage:\n/mavro')
                print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] ' + 'Help sent')
            else:
                try:
                    coin = command.replace('/', '')
                    coin = coin.lower()
                    result = price_get(db[coin])

                    name = result[0]
                    symbol = result[1]
                    rank = result[2]
                    price_usd = result[3]
                    price_btc = result[4]
                    volume_usd = result[5]
                    market_cap_usd = result[6]
                    available_supply = result[7]
                    total_supply = result[8]
                    max_supply = result[9]
                    percent_change_1h = result[10]
                    percent_change_24h = result[11]
                    percent_change_7d = result[12]
                    last_updated = result[13]


                    last_updated = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(last_updated)))


                    if volume_usd is None:
                        volume_usd = 'n/a'
                    else:
                        volume_usd = commas(int(float(volume_usd)))

                    if market_cap_usd is None:
                        market_cap_usd = 'n/a'
                    else:
                        market_cap_usd = commas(int(float(market_cap_usd)))

                    if available_supply is None:
                        available_supply = 'n/a'
                    else:
                        available_supply = commas(int(float(available_supply)))

                    if total_supply is None:
                        total_supply = 'n/a'
                    else:
                        total_supply = commas(int(float(total_supply)))

                    if max_supply is None:
                        max_supply = 'n/a'
                    else:
                        max_supply = commas(int(float(max_supply)))

                    if percent_change_1h is None:
                        percent_change_1h = 'n/a'
                        st1 = ''
                    elif float(percent_change_1h) >= 0:
                        st1 = '↗️'
                    else:
                        st1 = '↘️'

                    if percent_change_24h is None:
                        percent_change_24h = 'n/a'
                        st2 = ''
                    elif float(percent_change_24h) >= 0:
                        st2 = '↗️'
                    else:
                        st2 = '↘️'

                    if percent_change_7d is None:
                        percent_change_7d = 'n/a'
                        st3 = ''
                    elif float(percent_change_7d) >= 0:
                        st3 = '↗️'
                    else:
                        st3 = '↘️'

                    bot.sendMessage(chat_id, "ℹ️ *{}* - {}, rank: {} ({})\n▸ Price: *{}* $, {} Ƀ\n▸ Change %: {} {} 1h, {} {} 24h, {} {} 7d\n▸ Market Cap: {} $\n▸ 24h volume: {} $\n▸ Maximum supply: {}\n▸ Total: {}\n▸ Current: {}".format(name, symbol, rank, last_updated, price_usd, price_btc, st1, percent_change_1h, st2, percent_change_24h, st3, percent_change_7d, market_cap_usd, volume_usd, max_supply, total_supply, available_supply ), parse_mode = 'Markdown')
                    print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] ' + 'Price sent')
                except Exception as e:
                    print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] ' + 'ERROR: ' + str(e))

def apocalypse():
    while True:
        msi = telepot.message_identifier(bot.sendMessage(str(ch_id), quotes[random.randint(0, len(quotes) - 1)])) # movrodiy semi-silent revoke
        time.sleep(1)
        bot.deleteMessage(msi)
        #bot.deleteMessage(telepot.message_identifier(bot.sendMessage(str(ch_id), quotes[random.randint(0, len(quotes) - 1)])))
        print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'Movrodiy revoked')
        time.sleep(random.randint(150, 200))


print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'Waiting Movrodiy to be ready')

myThread = threading.Thread(target = price_update)
myThread.start()

myThread2 = threading.Thread(target = apocalypse)
myThread2.start()

time.sleep(8)


updates = bot.getUpdates()

if updates: # ignore old messages on initialization
    last_update_id = updates[-1]['update_id']
    bot.getUpdates(offset = last_update_id + 1)


MessageLoop(bot, handle).run_as_thread()
print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'Movrodiy ready')

while 1:
    time.sleep(10)
