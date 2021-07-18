#!/usr/bin/env python
# pylint: disable=W0603

import logging
from typing import NoReturn
from time import sleep

import json
from urllib import request

import telegram
from telegram.error import NetworkError, Unauthorized


UPDATE_ID = None



def start():
	return('Vem vindos ao bot local IP. apenas me envie um IP oy url e eu direi de onde ele é ou tá hospedado.')

def obter_json(ip):
#some JSON:
	urlr = request.urlopen("http://ip-api.com/json/"+ip+"?fields=1113821&lang=pt-BR").read()

# parse x:
	y = json.loads(urlr)

# the result is a Python dictionary:
	if(y["status"] == 'success'):
		final=('IP: '+str(y["query"])+'\nContinente: '+y["continent"]+'\nPaís: '+y["country"]+'\nEstado: '+y["regionName"]+', '+y["region"]+'\nCidade '+y["city"]+'\nProvedor: '+y["isp"]+'\nFornecedora: '+y["org"]+'\nLatitude '+str(y["lat"])+', Longitude '+str(y["lon"]))
		return(final)
	else:
		return('Nao foi possível verificar este IP, tente novamente')

def central(texto):
	if(texto == "/start"):
		star=start()
		return(star)
	else:
		lk=obter_json(texto)
		return (lk)

def main() -> NoReturn:
    """Run the bot."""
    global UPDATE_ID
    # Telegram Bot Authorization Token
    bot = telegram.Bot('')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        UPDATE_ID = bot.get_updates()[0].update_id
    except IndexError:
        UPDATE_ID = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            UPDATE_ID += 1


def echo(bot: telegram.Bot) -> None:
    """Echo the message the user sent."""
    global UPDATE_ID
    # Request updates after the last update_id
    for update in bot.get_updates(offset=UPDATE_ID, timeout=10):
        UPDATE_ID = update.update_id + 1

        # your bot can receive updates without messages
        # and not all messages contain text
        if update.message and update.message.text:
            # Reply to the message
            update.message.reply_text(central(update.message.text))


if __name__ == '__main__':
    main()
