import requests as r
import telegram
import json
import time
import shelve

from bs4 import BeautifulSoup as bs

check_site = "https://www.ansperformance.com/products/rave?variant=28223563464809"

state = shelve.open("./stockstatus.json")


def check_retailer(site):
    raw_page = r.get(site).content
    soup = bs(raw_page, "html.parser")
    button = soup.find(class_="sold-out__container").find(string="Sold Out")
    sold_out = not any(button) if button is not None else None
    # print(button)
    return sold_out


def notify_ending(message):
    with open('./docs/keys.json', 'r') as keys_file:
        k = json.load(keys_file)
        token = k['telegram_token']
        chat_id = k['telegram_chat_id']
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=message)


state['in_stock'] = False

while True:
    if "in_stock" not in state.keys():
        state['in_stock'] = False
    if check_retailer(check_site) is None and not state['in_stock']:
        notify_ending(f"In Stock {check_site}")
        state['in_stock'] = True
    else:
        state['in_stock'] = False
    state.sync()
    time.sleep(300)
