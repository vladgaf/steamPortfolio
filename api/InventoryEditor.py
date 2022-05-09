from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem
from peewee import DoesNotExist, JOIN
from peewee import fn
from api import InventoryReader
from api import CurrentPriceParser
from api import InventoryParser


def refreshInventory(user_id):
    queryList = UserItem.getUserItems(user_id)
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
            Item.createItem(name=key, price=CurrentPriceParser.parseItemPrice(key),
                            trend=CurrentPriceParser.parseItemTrend(key))
            #Item.createItem(name=key, price=CurrentPriceParser.parseItemPrice(key), trend="CurrentPriceParser.parseItemTrend(key)")
        finally:
            userItem = UserItem()
            user = User.select(User).where(User.id == user_id).get()
            item = Item.select().where(Item.itemName == str(key)).get()
            UserItem.createUserItem(userItem, user=user, item=item, quantity=raw_item["quantity"], boughtprice=raw_item["boughtPrice"])

def getTotalInvested(user_id):
    sum = UserItem.select(fn.SUM(UserItem.boughtPrice)).where(UserItem.user == user_id).dicts().get()
    return sum['sum']

def getTotalWorthNow(user_id):
    query = UserItem.select(fn.SUM(Item.currentPrice)).join(Item, on=(Item.id == UserItem.item)).where(UserItem.user==user_id).dicts().get()
    return query['sum']

#getTotalWorthNow(1)
