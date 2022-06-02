from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem
from peewee import DoesNotExist

from api import InventoryReader
from api import CurrentPriceParser


def refreshAllPrices():
    for item in Item.select():
        Item.update({"currentPrice": CurrentPriceParser.parseItemPrice(item.itemName)}).where(Item.id == item.id).execute()
        #Item.update({"priceTrend": CurrentPriceParser.parseItemTrend(item.itemName)}).where(Item.id == item.id).execute()

