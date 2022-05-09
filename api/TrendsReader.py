from peewee import DoesNotExist

from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem

from api import InventoryReader
from api import CurrentPriceParser

def extractTrendsByName(item_name):
    item = Item.getItemByName(item_name)
    trend_string = item.trend.split("; ")
    labels = []
    values = []
    for item in trend_string:
        item = item[1 : -1].split(', ')
        label = item[0]
        labels.append(label[1 : -1])
        values.append(float(item[1]))
    return labels, values

#print(extractTrendsByName("Souvenir MAC-10 | Palm (Well-Worn)")[0])