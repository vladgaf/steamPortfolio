from utils import Constants
from peewee import *

if __name__ == '__main__':
    pg_db = PostgresqlDatabase('steamPortfolio', user='postgres', password='1234', host='localhost', port=5432)
    pg_db.connect()
