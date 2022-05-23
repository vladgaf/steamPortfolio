import requests
import logging
import io
import xml.dom.minidom as xml_md

from colorama import Fore, Back, Style
from beans.User import User
from utils import Constants

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def validateLink(link):
    try:
        url_profile = link + '?xml=1'
        request_profile = requests.get(url=url_profile, headers=Constants.HEADERS)
        doc = xml_md.parse(io.StringIO(request_profile.content.decode("utf-8")))
        steam_id64 = doc.getElementsByTagName('steamID64')[0].childNodes[0].nodeValue
        return link
    except BaseException:
        return False


def profileLinkToSteamId64(link):
    try:
        url_profile = link + '?xml=1'
        request_profile = requests.get(url=url_profile, headers=Constants.HEADERS)
        doc = xml_md.parse(io.StringIO(request_profile.content.decode("utf-8")))
        steam_id64 = doc.getElementsByTagName('steamID64')[0].childNodes[0].nodeValue
        logging.debug(steam_id64)
        name = doc.getElementsByTagName('steamID')[0].childNodes[0].nodeValue
        user = User()
        if not User.select().where(User.userProfile == steam_id64).exists():
            user.createUser(steam_id64, name)
    except BaseException:
        logging.debug(Fore.RED + "Incorrect link, try again.")
    return steam_id64


def getInventoryArray(steam_id64):
    global itemsList
    url = 'https://steamcommunity.com/inventory/' + str(steam_id64) + '/730/2'
    request = requests.get(url=url, headers=Constants.HEADERS).json()
    if request is not None or request.json()["success"] is not False:
        itemsList = []
        for i in range(len(request['assets'])):
            for k in range(len(request['descriptions'])):
                if request['assets'][i]['classid'] == request['descriptions'][k]['classid']:
                    if request['descriptions'][k]['marketable'] == 1:
                        itemsList.append(request['descriptions'][k]['market_hash_name'])

    itemsArray = dict((x, itemsList.count(x)) for x in set(itemsList))
    #logging.debug(itemsArray)
    return itemsArray

