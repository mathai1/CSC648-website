from flask import Flask, render_template, request
import pymysql
from db import SFSU_DB
app = Flask(__name__)

db = SFSU_DB()


@app.route('/', methods=['GET'])
def home():
    users = db.getAllUsers()
    lst = getOrganizedData(users)
    return render_template("home.html", data = lst)

@app.route('/search', methods= ['GET' , 'POST'])
def search():
    if request.method == 'POST':
        category =request.form['filter']
        searchedData =request.form['searchedData']
        users = db.getAUser(category,searchedData)
        lst = getOrganizedData(users)
        return render_template("search.html", data = lst)
    return render_template("search.html")
    
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/about/<name>')
def getPerson(name):
    item = f"about/{name}.html"
    return render_template(item, name = name)


def getOrganizedData(users) :
    lst = []
    dUsers = {}
    for row in users:
        dUsers = {"email": row[0], "password":row[1], "fname":row[2], "lname":row[3], "image" : row[4]}
        lst.append(dUsers)
    return lst

