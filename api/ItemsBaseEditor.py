from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem
from peewee import DoesNotExist

import InventoryReader
import CurrentPriceParser


def refreshAllPrices():
    for item in Item.select():
        Item.update({"currentPrice": CurrentPriceParser.parseItemPrice(item.itemName)}).where(Item.id == item.id).execute()
