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

    def createUserItem(self, user, item, quantity, boughtprice):
        userItem = UserItem()
        userItem.user = user
        userItem.item = item
        userItem.quantity = quantity
        userItem.boughtPrice = boughtprice
        userItem.save()

        return userItem

    def updateBuyPrice(buy_price, user_id, item_id):
        query = UserItem.update({"boughtPrice": buy_price}).where(UserItem.user == user_id, UserItem.item == item_id)
        print(query.sql)
        return query.execute()

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






