from peewee import *

pg_db = PostgresqlDatabase('steamPortfolio', user='postgres', password='1234', host='localhost', port=5432)

class User(Model):
    userProfile = CharField()
    userName = CharField()

    class Meta:
        database = pg_db


    def createUser(self, profile, userName):
        user = User()
        user.userProfile = profile
        user.userName = userName
        user.save()
        return user

    @staticmethod
    def getUserBySteamId64(steam_Id64):
        user = User.select(User).where(User.userProfile == steam_Id64).get()
        return user
