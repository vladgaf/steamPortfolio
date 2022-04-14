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

from beans.User import User

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/37.0.2062.120 Safari/537.36'}


def getInventoryArray():
    print(Fore.BLUE + "Paste your profile link, for example:\nhttps://steamcommunity.com"
                       "/id/yourcustomid/\nhttps://steamcommunity.com"
                       "/profiles/7*************/")
    correct_link = False
    while not correct_link:
        try:
            url_profile = input() + '?xml=1'
            request_profile = requests.get(url=url_profile, headers=headers)
            doc = xml_md.parse(io.StringIO(request_profile.content.decode("utf-8")))
            steam_id64 = doc.getElementsByTagName('steamID64')[0].childNodes[0].nodeValue
            print(steam_id64)
            user = User()
            if not User.select().where(User.userProfile == steam_id64).exists():
                user.createUser(steam_id64)
            correct_link = True
        except IndexError:
            correct_link = False
            print(Fore.RED + "Incorrect link, try again.")
        except requests.exceptions.MissingSchema:
            correct_link = False
            print(Fore.RED + "Incorrect link, try again.")
        except requests.exceptions.ProxyError:
            correct_link = False
            print(Fore.RED + "Incorrect link, try again.")
        except UnboundLocalError:
            correct_link = False
            print(Fore.RED + "Incorrect link, try again.")
        except requests.exceptions.InvalidURL:
            correct_link = False
            print(Fore.RED + "Incorrect link, try again.")

    url = 'https://steamcommunity.com/inventory/' + steam_id64 + '/730/2'
    request = requests.get(url=url, headers=headers).json()
    if request is not None or request.json()["success"] is not False:
        itemsList = []
        for i in range(len(request['assets'])):
            for k in range(len(request['descriptions'])):
                if request['assets'][i]['classid'] == request['descriptions'][k]['classid']:
                    if request['descriptions'][k]['marketable'] == 1:
                        itemsList.append(request['descriptions'][k]['market_hash_name'])

    itemsArray = dict((x, itemsList.count(x)) for x in set(itemsList))
    print(itemsArray)
    return itemsArray
