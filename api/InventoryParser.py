from peewee import DoesNotExist

from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem

from colorama import Fore

from api import InventoryReader
from api import CurrentPriceParser


def parseUserItems(steam_id64):
    #steam_id64 = InventoryReader.profileLinkToSteamId64()
    itemsDict = InventoryReader.getInventoryArray(steam_id64)
    for item_name in itemsDict.keys():
        #print(item_name)
        try:
            Item.select(Item).where(Item.itemName == str(item_name)).get()
        except (DoesNotExist, IndexError):
            item = Item()
            print("Parse exception")
            item.createItem(item_name, CurrentPriceParser.parseItemPrice(item_name), CurrentPriceParser.parseItemTrend(item_name))
            #item.createItem(item_name, CurrentPriceParser.parseItemPrice(item_name), "CurrentPriceParser.parseItemTrend(item_name)")
        finally:
            userItem = UserItem()
            user = User.select(User).where(User.userProfile == steam_id64).get()
            item = Item.select(Item).where(Item.itemName == str(item_name)).get()
            userItem.createUserItem(user, item, itemsDict[item_name], 0.0)



# InventoryReader.profileLinkToSteamId64("https://steamcommunity.com/profiles/76561198308132032")
# parseUserItems(76561198308132032)
