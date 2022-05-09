from peewee import *

pg_db = PostgresqlDatabase('steamPortfolio', user='postgres', password='1234', host='localhost', port=5432)


class Item(Model):
    itemName = CharField()
    currentPrice = FloatField()
    trend = CharField(max_length = 1000)

    class Meta:
        database = pg_db

    @staticmethod
    def createItem(name, price, trend):
        item = Item()
        item.itemName = name
        item.currentPrice = price
        item.trend = trend
        item.save()
        return item

    @staticmethod
    def getItemByName(name):
        item = Item.select(Item).where(Item.itemName == name).get()
        return item
