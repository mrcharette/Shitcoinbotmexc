import requests
import time
import os
from telegram import Bot

bot = Bot(token=os.environ['BOT_TOKEN'])
chat_id = os.environ['CHAT_ID']

def get_tokens():
    url = "https://pump.fun/_trpc/feed.getTokens?batch=1&input=%7B%220%22%3A%7B%22sort%22%3A%22recent%22%7D%7D"
    headers = {"origin": "https://pump.fun"}
    try:
        response = requests.get(url, headers=headers)
        tokens = response.json()['data'][0]['result']['data']['tokens']
        return tokens
    except:
        return []

sent = set()

def is_valid(token):
    try:
        return (
            token['liquidity'] > 2000 and
            token['buyTax'] == 0 and
            token['sellTax'] == 0 and
            not token['mintable']
        )
    except:
        return False

while True:
    tokens = get_tokens()
    for token in tokens:
        token_id = token['id']
        if token_id in sent:
            continue
        if is_valid(token):
            msg = f"💥 Nouveau token : {token['name']}\n💧 Liquidité : ${token['liquidity']}\n🔗 https://pump.fun/{token_id}"
            bot.send_message(chat_id=chat_id, text=msg)
            sent.add(token_id)
    time.sleep(30)
