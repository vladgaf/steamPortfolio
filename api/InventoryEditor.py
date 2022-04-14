from beans.Item import Item
from beans.User import User
from beans.UserItem import UserItem

import InventoryReader
import CurrentPriceParser
import InventoryParser


#UserItem.updateBoughtPrice(UserItem.select(UserItem).where(UserItem.item == item))