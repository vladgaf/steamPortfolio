import InventoryReader
from peewee import DoesNotExist
import os
import os.path
import warnings
import datetime
import time
import requests
import json
import re
import io
import xml.dom.minidom as xml_md
import urllib.parse
import colorama
from colorama import Fore, Back, Style

from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem

from utils import Constants


def linkbulider(market_hash_name):
    market_hash_name = market_hash_name.replace('%E2%98%85', "★")
    market_hash_name = market_hash_name.replace('%E2%84%A2', "™")
    steam_apis_parse_link = "https://api.steamapis.com/market/item/730/" + urllib.parse.quote(
        market_hash_name) + "?api_key=" + Constants.STEAM_APIS_API_KEY
    steam_market_link = 'https://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=' + urllib.parse.quote(
        market_hash_name)
    return steam_market_link, steam_apis_parse_link


def getPriceViaSteamMarket(name):
    link = linkbulider(name)[0]
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
    link = linkbulider(name)[1]
    print(link)
    response = requests.get(url=link, headers=Constants.HEADERS)
    print(response.json())
    try:
        if response.json()['status'] == 402:
            raise Exception("AddFundsException")
    except KeyError:
        price = response.json()['median_avg_prices_15days'][-1][1]
        return round(price, 2)


def parseItemPrice(item_name):
    try:
        return getPriceViaSteamApis(item_name)
    except (Exception("AddFundsException"), BaseException):
        return getPriceViaSteamMarket(item_name)


itemsDict = InventoryReader.getInventoryArray()


def parseItems(itemsDict):
    for item_name in itemsDict.keys():
        print(item_name)
        try:
            item = Item.select(Item).where(Item.itemName == str(item_name)).get()
        except DoesNotExist:
            item = Item()
            item.createItem(item_name, parseItemPrice(item_name))
        finally:
            userItem = UserItem()
            user = User.select(User).where(User.userProfile == "76561198156800409").get() #как поднимать юзера который об этой хуйне попросил?
            item = Item.select().where(Item.itemName == str(item_name)).get()
            userItem.createUserItem(user, item, itemsDict[item_name])


parseItems(itemsDict)
