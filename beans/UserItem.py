from peewee import *

from beans.Item import Item
from beans.User import User

pg_db = PostgresqlDatabase('steamPortfolio', user='postgres', password='1234', host='localhost', port=5432)


class UserItem(Model):
    user = ForeignKeyField(User)
    item = ForeignKeyField(Item)
    quantity = IntegerField()
    boughtPrice = FloatField(null=True)

    class Meta:
        database = pg_db

    def createUserItem(self, user, item, quantity):
        userItem = UserItem()
        userItem.user = user
        userItem.item = item
        userItem.quantity = quantity
        #userItem.boughtPrice = 0.0 # ограничение notNull он совсем ебанулся?
        userItem.save()

        return userItem

    def updateBoughtPrice(self, boughtPrice):
        self.boughtPrice = boughtPrice
        self.save()

    def getUserItems(id):
        try:
            return (UserItem
                .select(UserItem, User, Item)
                .join(User)
                .switch(UserItem)
                .join(Item)
                .where(User.id == id)
                .dicts())
        except DoesNotExist:
            print("NotFound")

    def getUserItem(self, steamid_64, name):
        userItemsDict = self.getUserItems(steamid_64)


