from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem
from peewee import DoesNotExist

import InventoryReader
import CurrentPriceParser
import InventoryParser


def refreshInventory(user_id):
    queryList = UserItem.getUserItems(1)
    queryDict = {}
    for item in queryList:
        queryDict[item['itemName']] = {"quantity": item['quantity'], "boughtPrice": item['boughtPrice']}
    inventoryDict = InventoryReader.getInventoryArray(User.select(User).where(User.id == user_id).get().userProfile)
    print(inventoryDict)
    print(queryDict)
    UserItem.delete().where(UserItem.user == user_id).execute()

    for key in inventoryDict.keys():
        raw_item = None
        if key in queryDict:
            raw_item = queryDict[key]
        else:
            raw_item = {"quantity": inventoryDict[key], "boughtPrice": 0}
        try:
            Item.select().where(Item.itemName == str(key)).get()
            #print(Item.select().where(Item.itemName == str(key)))
        except (DoesNotExist, IndexError):
            Item.createItem(name=key, price=CurrentPriceParser.parseItemPrice(key))
        finally:
            user = User.select(User).where(User.id == user_id).get()
            item = Item.select().where(Item.itemName == str(key)).get()
            UserItem.createUserItem(user=user, item=item, quantity=raw_item["quantity"], boughtprice=raw_item["boughtPrice"])
