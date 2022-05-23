from peewee import *
from peewee import DoesNotExist

from beans.Item import Item
from beans.User import User

from datetime import date

pg_db = PostgresqlDatabase('steamPortfolio', user='postgres', password='1234', host='localhost', port=5432)


class UserPortfolioLog(Model):
    user = ForeignKeyField(User)
    timestamp = CharField()
    totalWorth = FloatField(null=True)

    class Meta:
        database = pg_db

    @staticmethod
    def createUserPortfolioLog(user, totalWorth):
        userPortfolioLog = UserPortfolioLog()
        try:
            userPortfolioLog.select().where(user.id == User.id).where(UserPortfolioLog.timestamp == date.today())
        except DoesNotExist:
            userPortfolioLog.user = user
            userPortfolioLog.totalWorth = totalWorth
            userPortfolioLog.timestamp = date.today()
            userPortfolioLog.save()
        return userPortfolioLog

    @staticmethod
    def getUserPortfolioLogByID(user_id):
        timestamps = []
        values = []
        userPortfolioLog = UserPortfolioLog.select().where(UserPortfolioLog.user == user_id).dicts()
        for item in userPortfolioLog:
            timestamps.append(item['timestamp'])
            values.append(item['totalWorth'])
        return timestamps, values
