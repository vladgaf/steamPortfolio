from peewee import *

pg_db = PostgresqlDatabase('steamPortfolio', user='postgres', password='1234', host='localhost', port=5432)

class User(Model):
    userProfile = CharField()

    class Meta:
        database = pg_db

    def createUser(self, profile):
        user = User()
        user.userProfile = profile
        user.save()
        return user