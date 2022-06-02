import os
import statistics

from api import InventoryReader
from api import InventoryParser
from api import InventoryEditor
from api import ItemsBaseEditor
from api import CurrentPriceParser
from api import TrendsReader
from utils import Constants

from api import *
from peewee import *
from utils import TableCreator
from flask import Flask, render_template, request, url_for, redirect
from beans.User import User
from beans.UserItem import UserItem
from beans.Item import Item
from beans.UserPortfolioLog import UserPortfolioLog

from flask import send_from_directory

import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['post', 'get'])
def index():
    if request.method == 'GET':
        return render_template("main.html")
    if request.method == 'POST':
        steamLink = request.form.get('steamLink')
        if InventoryReader.validateLink(steamLink):
            logging.debug(steamLink) # запрос к данным формы
            steam_id64 = InventoryReader.profileLinkToSteamId64(steamLink)
            return redirect(url_for('usertable', steamID64=steam_id64))
        else:
            return render_template("main.html", message=Constants.INCORRECT_LINK_MESSAGE)


@app.route("/", methods=['post', 'get'])
@app.route("/<int:steamID64>", methods=['GET', 'POST'])
def usertable(steamID64):
    user = User.getUserBySteamId64(steamID64)
    if request.method == "GET":
        #logging.debug(type(steamID64))
        userItems = UserItem.getUserItems(user.id)
        if not userItems:
            logging.debug("ParsingItems")
            InventoryParser.parseUserItems(steamID64)
            userItems = UserItem.getUserItems(user.id)
        #logging.debug(*userItems, sep='\n')
        totalInvested = InventoryEditor.getTotalInvested(user.id)
        totalWorthNow = InventoryEditor.getTotalWorthNow(user.id)
        userStats = UserPortfolioLog.getUserPortfolioLogByID(user.id)
        return render_template("table.html", userItems = userItems, totalInvested=totalInvested, totalWorthNow=totalWorthNow, labels=userStats[0], values=userStats[1],
                               max = totalWorthNow * 1.3)
    if request.method == "POST":
        logging.debug(request.form)
        if 'refreshInventory' in request.form:
            InventoryEditor.refreshInventory(user.id)
            userItems = UserItem.getUserItems(user.id)
            totalInvested = InventoryEditor.getTotalInvested(user.id)
            totalWorthNow = InventoryEditor.getTotalWorthNow(user.id)
            userStats = UserPortfolioLog.getUserPortfolioLogByID(user.id)
            return render_template("table.html", userItems=userItems, totalInvested=totalInvested, totalWorthNow=totalWorthNow, labels=userStats[0], values=userStats[1],
                               max = totalWorthNow * 1.3)
        elif 'refreshPrices' in request.form:
            ItemsBaseEditor.refreshAllPrices()
            userItems = UserItem.getUserItems(user.id)
            totalInvested = InventoryEditor.getTotalInvested(user.id)
            totalWorthNow = InventoryEditor.getTotalWorthNow(user.id)
            userStats = UserPortfolioLog.getUserPortfolioLogByID(user.id)
            return render_template("table.html", userItems=userItems, totalInvested=totalInvested, totalWorthNow=totalWorthNow, labels=userStats[0], values=userStats[1],
                               max = totalWorthNow * 1.3)
        elif 'boughtPrice' in request.form:
            # logging.debug("Name:" + request.form.get('itemName'))
            # logging.debug("BP:" + request.form.get('boughtPrice'))
            user = User.getUserBySteamId64(steamID64)
            item = Item.getItemByName(request.form.get('itemName'))
            bought_price = float(request.form.get('boughtPrice'))
            UserItem.updateBuyPrice(bought_price, user.id, item.id)
            userItems = UserItem.getUserItems(user.id)
            totalInvested = InventoryEditor.getTotalInvested(user.id)
            totalWorthNow = InventoryEditor.getTotalWorthNow(user.id)
            return render_template("table.html", userItems=userItems, totalInvested=totalInvested, totalWorthNow=totalWorthNow)
        elif 'itemDetails' in request.form:
            return redirect(url_for('itemStats', itemName=request.form.get('itemName')))
        elif 'steamLink' in request.form:
            steamLink = request.form.get('steamLink')
            if InventoryReader.validateLink(steamLink):
                logging.debug(steamLink)  # запрос к данным формы
                steam_id64 = InventoryReader.profileLinkToSteamId64(steamLink)
                return redirect(url_for('usertable', steamID64=steam_id64))
            else:
                return render_template("main.html", message=Constants.INCORRECT_LINK_MESSAGE)
        else:
            pass


@app.route("/<string:itemName>", methods=['GET', 'POST'])
def itemStats(itemName):
    if request.method == 'GET':
        price_trend = TrendsReader.extractTrendsByName(itemName)
        logging.debug(price_trend[0])
        logging.debug(price_trend[1])
        bar_labels = price_trend[0]
        bar_values = price_trend[1]
        max_chart_value = max(bar_values)
        average_price = statistics.mean(bar_values)
        current_price = price_trend[1][-1]
        market_link = CurrentPriceParser.generateMarketLink(itemName)
        logging.debug(average_price)
        return render_template("itempage.html", max=max_chart_value, itemName = itemName, title = "PriceGraph",
                               labels=bar_labels, values=bar_values, averagePrice = average_price, currentPrice = current_price, marketLink = market_link)


@app.route('/database', methods=['GET', 'POST'])
def database():
    if request.method == 'GET':
        return render_template('database.html')
    if request.method == 'POST':
        itemName = request.form.get('itemName')
        try:
            item = Item.getItemByName(itemName)
            return redirect(url_for('itemStats', itemName=request.form.get('itemName')))
        except BaseException:
            return render_template('database.html', message = Constants.INCORRECT_ITEM_MESSAGE)
    return

if __name__ == '__main__':
    app.run(debug=True,  host="0.0.0.0", port=8000)



