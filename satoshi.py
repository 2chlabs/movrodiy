# coding: utf8
# @ru2chcc


import telebot
import requests
import threading
import time


banner = r"""
 __  __   ___ __     __ ____    ___   ____  ___ __   __
|  \/  | / _ \\ \   / /|  _ \  / _ \ |  _ \|_ _|\ \ / /
| |\/| || | | |\ \ / / | |_) || | | || | | || |  \ V /
| |  | || |_| | \ V /  |  _ < | |_| || |_| || |   | |
|_|  |_| \___/   \_/   |_| \_\ \___/ |____/|___|  |_|

"""


print(banner)
print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'Movrodiy initialized')


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

        time.sleep(75)

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


bot = telebot.TeleBot('token', threaded = False) # paste your token here
user = bot.get_me()


@bot.message_handler(commands = ['help'])
def print_help(message):
    if message.chat.id == -1001383331161:
        print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] ' + 'Help requested')
        bot.reply_to(message, "Usage:\n/mavro")
        print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'Help sent')


myThread = threading.Thread(target = price_update)
myThread.start()


@bot.message_handler(func = lambda m: True)
def all_price(message):
    if message.text[0] == '/' and message.chat.id == -1001383331161: # lock to one chat
        try:
            coin = message.text.replace('/', '')
            coin = coin.lower()
            print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'Price requested')
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


            bot.reply_to(message, "ℹ️ *{}* - {}, rank: {} ({})\n▸ Price: *{}* $, {} Ƀ\n▸ Change %: {} {} 1h, {} {} 24h, {} {} 7d\n▸ Market Cap: {} $\n▸ 24h volume: {} $\n▸ Maximum supply: {}\n▸ Total: {}\n▸ Current: {}".format(name, symbol, rank, last_updated, price_usd, price_btc, st1, percent_change_1h, st2, percent_change_24h, st3, percent_change_7d, market_cap_usd, volume_usd, max_supply, total_supply, available_supply ), parse_mode = 'Markdown')
            print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'Price sent')
        except Exception as e:
            print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] '+ 'ERROR: '+ str(e))


while True:
    try:
        bot.polling()
    except Exception as f:
        print('MOVRODIY DIED')

        print('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] ' + 'CRITICAL ERROR: ' + str(f))
        critical = open('critical_log.txt', 'w')
        critical.write('[' + time.strftime("%H:%M:%S", time.localtime(time.time())) + '] ' + 'CRITICAL ERROR: ' + str(f))
        critical.close()

        print('Restarting Movrodiy')
        time.sleep(15)
        print('Movrodiy initialized')
