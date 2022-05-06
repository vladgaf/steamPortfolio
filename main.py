from api import InventoryReader
from api import InventoryParser
from api import InventoryEditor
from api import ItemsBaseEditor
from utils import Constants
from api import *
from peewee import *
from utils import TableCreator
from flask import Flask, render_template, request, url_for, redirect
from beans.User import User
from beans.UserItem import UserItem
from beans.Item import Item

app = Flask(__name__)


@app.route("/", methods=['post', 'get'])
def foo():
    if request.method == 'GET':
        return render_template("main.html")
    if request.method == 'POST':
        steamLink = request.form.get('steamLink')
        if InventoryReader.validateLink(steamLink):
            print(steamLink) # запрос к данным формы
            steam_id64 = InventoryReader.profileLinkToSteamId64(steamLink)
            return redirect(url_for('usertable', steamID64=steam_id64))
        else:
            return render_template("main.html", message=Constants.INCORRECT_LINK_MESSAGE)


@app.route("/", methods=['post', 'get'])
@app.route("/<int:steamID64>", methods=['GET', 'POST'])
def usertable(steamID64):
    user = User.getUserBySteamId64(steamID64)
    if request.method == "GET":
        #print(type(steamID64))
        userItems = UserItem.getUserItems(user.id)
        if not userItems:
            print("ParsingItems")
            InventoryParser.parseUserItems(steamID64)
            userItems = UserItem.getUserItems(user.id)
        #print(*userItems, sep='\n')
        totalInvested = InventoryEditor.getTotalInvested(user.id)
        totalWorthNow = InventoryEditor.getTotalWorthNow(user.id)
        return render_template("table.html", userItems = userItems, totalInvested=totalInvested, totalWorthNow=totalWorthNow)
    if request.method == "POST":
        print()
        if 'refreshInventory' in request.form:
            InventoryEditor.refreshInventory(user.id)
            userItems = UserItem.getUserItems(user.id)
            return render_template("table.html", userItems=userItems)
        elif 'refreshPrices' in request.form:
            ItemsBaseEditor.refreshAllPrices()
            userItems = UserItem.getUserItems(user.id)
            return render_template("table.html", userItems=userItems)
        else:
            # print("Name:" + request.form.get('itemName'))
            # print("BP:" + request.form.get('boughtPrice'))
            user = User.getUserBySteamId64(steamID64)
            item = Item.getItemByName(request.form.get('itemName'))
            bought_price = float(request.form.get('boughtPrice'))
            UserItem.updateBuyPrice(bought_price, user.id, item.id)
            userItems = UserItem.getUserItems(user.id)
            totalInvested = InventoryEditor.getTotalInvested(user.id)
            totalWorthNow = InventoryEditor.getTotalWorthNow(user.id)
            return render_template("table.html", userItems=userItems, totalInvested=totalInvested, totalWorthNow=totalWorthNow)



if __name__ == '__main__':
    app.run(debug=True,  host="0.0.0.0", port=8000)



