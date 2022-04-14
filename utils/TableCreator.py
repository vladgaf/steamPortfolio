from peewee import *
from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem

def createTables():
    pg_db = PostgresqlDatabase('steamPortfolio', user='postgres', password='1234', host='localhost', port=5432)
    pg_db.create_tables([Item, User, UserItem])

def dropTables():
    Item.drop_table()
    User.drop_table()
    UserItem.drop_table()

createTables()