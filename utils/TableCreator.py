from peewee import *
from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem

pg_db = PostgresqlDatabase('steamPortfolio', user='postgres', password='1234', host='localhost', port=5432)
pg_db.create_tables([Item, User, UserItem])