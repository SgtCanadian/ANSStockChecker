import requests as r
import telegram
import time
import shelve
import os

from bs4 import BeautifulSoup as bs
from configparser import ConfigParser

config_dir = os.path.normpath(os.getenv("CONFIG_PATH", f"{os.getcwd()}/config"))
config = ConfigParser()
config_file = os.path.normpath(f"{config_dir}/config.ini")
if os.path.isfile(config_file):
    config.read(config_file)

check_site = os.getenv("CHECK_URL", config.get("app", "url"))

state = shelve.open(os.path.normpath(f"{config_dir}/stockstatus.json"))


def check_retailer(site):
    raw_page = r.get(site).content
    soup = bs(raw_page, "html.parser")
    button = soup.find(class_="sold-out__container").find(string="Sold Out")
    sold_out = not any(button) if button is not None else None
    # print(button)
    return sold_out


def notify_ending(message):
    bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN", config.get("telegram", "tokenid")))
    bot.sendMessage(chat_id=os.getenv("TELEGRAM_CHATID", config.get("telegram", "chatid")), text=message)


while True:
    if "in_stock" not in state.keys():
        state['in_stock'] = False
    if check_retailer(check_site) is None and not state['in_stock']:
        message = os.getenv("NOTIFY_MESSAGE", config.get("app", "message"))
        notify_ending(f"{message}\n{check_site}")
        state['in_stock'] = True
    else:
        state['in_stock'] = False
    state.sync()
    time.sleep(int(os.getenv("REFRESH_SEC", config.get("app", "refresh"))))
