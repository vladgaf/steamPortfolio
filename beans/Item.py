from peewee import *

pg_db = PostgresqlDatabase('steamPortfolio', user='postgres', password='1234', host='localhost', port=5432)


class Item(Model):
    itemName = CharField()
    currentPrice = FloatField()

    class Meta:
        database = pg_db

    def createItem(self, name, price):
        item = Item()
        item.itemName = name
        item.currentPrice = price
        item.save()
        return item

    def getItemByName(name):
        item = Item.select(Item).where(Item.itemName == name).get()
        return item
