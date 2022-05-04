from api import InventoryReader
from utils import Constants
from api import *
from peewee import *
from utils import TableCreator
from flask import Flask, render_template, request, url_for, redirect
from beans.User import User
from beans.UserItem import UserItem
from beans.Item import Item

app = Flask(__name__)



dictionary = {'quantity': 1, 'boughtPrice': 0.0, 'itemName': 'Souvenir Sawed-Off | Irradiated Alert (Battle-Scarred)', 'currentPrice': 0.39}


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


@app.route("/<int:steamID64>")
def usertable(steamID64):
    user = User.getUserBySteamId64(steamID64)
    userItems = UserItem.getUserItems(User.id)
    for item in userItems:
        del item["user"]
        del item["item"]
        del item['userProfile']
        del item["id"]
        print(item)
    #return render_template("table.html", tables=[df.to_html(classes='data')], titles=df.columns.values)
    return render_template("table.html", userItems = userItems)


if __name__ == '__main__':
    app.run(debug=True,  host="0.0.0.0", port=8000)



