from peewee import DoesNotExist

from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem
from beans.UserPortfolioLog import UserPortfolioLog

from colorama import Fore

from api import InventoryReader
from api import CurrentPriceParser
from api import InventoryEditor

import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def parseUserItems(steam_id64):
    #steam_id64 = InventoryReader.profileLinkToSteamId64()
    itemsDict = InventoryReader.getInventoryArray(steam_id64)
    for item_name in itemsDict.keys():
        #logging.debug(item_name)
        try:
            Item.select(Item).where(Item.itemName == str(item_name)).get()
        except (DoesNotExist, IndexError):
            item = Item()
            logging.debug("Parse exception")
            item.createItem(item_name, CurrentPriceParser.parseItemPrice(item_name), CurrentPriceParser.parseItemTrend(item_name))
            #item.createItem(item_name, CurrentPriceParser.parseItemPrice(item_name), "CurrentPriceParser.parseItemTrend(item_name)")
        finally:
            userItem = UserItem()
            user = User.select(User).where(User.userProfile == steam_id64).get()
            item = Item.select(Item).where(Item.itemName == str(item_name)).get()
            userItem.createUserItem(user, item, itemsDict[item_name], 0.0)

    UserPortfolioLog.createUserPortfolioLog(User.getUserBySteamId64(steam_id64), InventoryEditor.getTotalWorthNow(User.getUserBySteamId64(steam_id64).id))



# InventoryReader.profileLinkToSteamId64("https://steamcommunity.com/profiles/76561198308132032")
# parseUserItems(76561198308132032)
