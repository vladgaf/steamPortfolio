import datetime

import logging
import requests
import json
import urllib.parse
from datetime import date

from colorama import Fore, Back, Style
from utils import Constants
from utils import CommonUtils

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def generateMarketLink(market_hash_name):
    return "https://steamcommunity.com/market/listings/730/" + urllib.parse.quote(market_hash_name)


def linkBuilder(market_hash_name):
    market_hash_name = market_hash_name.replace('%E2%98%85', "★")
    market_hash_name = market_hash_name.replace('%E2%84%A2', "™")
    steam_apis_parse_link = "https://api.steamapis.com/market/item/730/" + urllib.parse.quote(
        market_hash_name) + "?api_key=" + Constants.STEAM_APIS_API_KEY
    steam_market_link = 'https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=' + urllib.parse.quote(
        market_hash_name)
    return steam_market_link, steam_apis_parse_link


def getPriceViaSteamMarket(name):
    link = linkBuilder(name)[0]
    logging.debug(link)
    response = requests.get(url=link, headers=Constants.HEADERS)
    try:
        return response.json()['lowest_price'][1:].replace(',', '.')
    except KeyError:
        logging.debug(Fore.RED + "Request Error, try again later...")
    except TypeError:
        logging.debug(Fore.RED + "Steam Error 429, try again later...")
    except json.decoder.JSONDecodeError:
        logging.debug(Fore.RED + "Steam is not responding, visit https://steamstat.us/ for check aviability")


def getPriceViaSteamApis(name):
    link = linkBuilder(name)[1]
    logging.debug(link)
    response = requests.get(url=link, headers=Constants.HEADERS)
    logging.debug(response.json())
    try:
        if response.json()['status'] == 402:
            raise Exception("AddFundsException")
    except KeyError:
        price = response.json()['median_avg_prices_15days'][-1][1]
        logging.debug("Item name:" + name + "Item Price" + str(price))
        return round(price, 2)


def parseItemPrice(item_name):
    try:
        return getPriceViaSteamApis(item_name)
    except (Exception("AddFundsException"), BaseException):
        return getPriceViaSteamMarket(item_name)




def parseItemTrend(name):
    link = linkBuilder(name)[1]
    logging.debug(link)
    response = requests.get(url=link, headers=Constants.HEADERS)
    logging.debug(response.json())
    try:
        if response.json()['status'] == 402:
            return "[" + str(datetime.date.today()) + ", " + getPriceViaSteamMarket(name) +"];"
    except KeyError:
        trend = response.json()['median_avg_prices_15days']
        for item in trend:
            item.remove(item[2])
            item[1] = round(item[1], 2)
    return CommonUtils.listToStr(trend, '; ')


#logging.debug(parseItemTrend("MAC-10 | Heat (Field-Tested)"))