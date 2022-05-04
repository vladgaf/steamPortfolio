from peewee import DoesNotExist

from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem

import InventoryReader
import CurrentPriceParser


def parseUserItems():
    steam_id64 = InventoryReader.profileLinkToSteamId64()
    itemsDict = InventoryReader.getInventoryArray(steam_id64)
    for item_name in itemsDict.keys():
        #print(item_name)
        try:
            Item.select(Item).where(Item.itemName == str(item_name)).get()
        except DoesNotExist:
            item = Item()
            item.createItem(item_name, CurrentPriceParser.parseItemPrice(item_name))
        finally:
            userItem = UserItem()
            user = User.select(User).where(User.userProfile == steam_id64).get()
            item = Item.select().where(Item.itemName == str(item_name)).get()
            userItem.createUserItem(user, item, itemsDict[item_name], None)

#parseUserItems()
