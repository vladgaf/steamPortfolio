import requests
import json
import urllib.parse
from colorama import Fore, Back, Style
from utils import Constants


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
    print(link)
    response = requests.get(url=link, headers=Constants.HEADERS)
    try:
        return response.json()['lowest_price'][1:].replace(',', '.')
    except KeyError:
        print(Fore.RED + "Request Error, try again later...")
    except TypeError:
        print(Fore.RED + "Steam Error 429, try again later...")
    except json.decoder.JSONDecodeError:
        print(Fore.RED + "Steam is not responding, visit https://steamstat.us/ for check aviability")


def getPriceViaSteamApis(name):
    link = linkBuilder(name)[1]
    print(link)
    response = requests.get(url=link, headers=Constants.HEADERS)
    print(response.json())
    try:
        if response.json()['status'] == 402:
            raise Exception("AddFundsException")
    except KeyError:
        price = response.json()['median_avg_prices_15days'][-1][1]
        print("Item name:" + name + "Item Price" + str(price))
        return round(price, 2)


def parseItemPrice(item_name):
    try:
        return getPriceViaSteamApis(item_name)
    except (Exception("AddFundsException"), BaseException):
        return getPriceViaSteamMarket(item_name)