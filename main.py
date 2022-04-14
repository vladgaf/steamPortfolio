from utils import Constants
from api import InventoryParser
from api import InventoryReader
from api import InventoryEditor
from peewee import *
from utils import TableCreator


if __name__ == '__main__':
    TableCreator.createTables()
    InventoryParser.parseUserItems()


