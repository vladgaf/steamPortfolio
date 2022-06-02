from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem
from beans.UserPortfolioLog import UserPortfolioLog
from peewee import DoesNotExist, JOIN
from peewee import fn
from api import InventoryReader
from api import CurrentPriceParser
from api import InventoryParser
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def refreshInventory(user_id):
    user = User.select(User).where(User.id == user_id).get()
    queryList = UserItem.getUserItems(user_id)
    queryDict = {}
    for item in queryList:
        queryDict[item['itemName']] = {"quantity": item['quantity'], "boughtPrice": item['boughtPrice']}
    inventoryDict = InventoryReader.getInventoryArray(User.select(User).where(User.id == user_id).get().userProfile)
    logging.debug(inventoryDict)
    logging.debug(queryDict)
    UserItem.delete().where(UserItem.user == user_id).execute()

    for key in inventoryDict.keys():
        raw_item = None
        if key in queryDict:
            raw_item = queryDict[key]
        else:
            raw_item = {"quantity": inventoryDict[key], "boughtPrice": 0}
        try:
            Item.select().where(Item.itemName == str(key)).get()
        except (DoesNotExist, IndexError):
            Item.createItem(name=key, price=CurrentPriceParser.parseItemPrice(key),
                            trend=CurrentPriceParser.parseItemTrend(key))
        finally:
            userItem = UserItem()
            item = Item.select().where(Item.itemName == str(key)).get()
            UserItem.createUserItem(userItem, user=user, item=item, quantity=raw_item["quantity"], boughtprice=raw_item["boughtPrice"])

    UserPortfolioLog.createUserPortfolioLog(user, getTotalWorthNow(user.id))

def getTotalInvested(user_id):
    sum = UserItem.select(fn.SUM(UserItem.boughtPrice * UserItem.quantity)).where(UserItem.user == user_id).dicts().get()
    return sum['sum']

def getTotalWorthNow(user_id):
    query = UserItem.select(fn.SUM(Item.currentPrice * UserItem.quantity)).join(Item, on=(Item.id == UserItem.item)).where(UserItem.user==user_id).dicts().get()
    return query['sum']

