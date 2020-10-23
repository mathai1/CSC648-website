from flask import Flask, render_template, request
import pymysql
from search import SearchingDB
app = Flask(__name__)

db = SearchingDB()


@app.route('/', methods=['GET'])
def home():
    postings = db.getAllPostings()
    lst = getPostingOrganizedData(postings)
    return render_template("home.html", data = lst)

@app.route('/search', methods= ['GET' , 'POST'])
def search():
    if request.method == 'POST':
        category =request.form['filter']
        searchedData =request.form['searchedData']
        postings = db.searchAPosting(category,searchedData)
        lst = getPostingOrganizedData(postings)
        return render_template("search.html", data = lst)
    return render_template("search.html")
    
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/about/<name>')
def getPerson(name):
    item = f"about/{name}.html"
    return render_template(item, name = name)


def getUserOrganizedData(users) :
    lst = []
    dUsers = {}
    for row in users:
        dUsers = {"email": row[0], "password":row[1], "fname":row[2], "lname":row[3], "image" : row[4]}
        lst.append(dUsers)
    return lst

def getPostingOrganizedData(postings) :
    lst = []
    dPosting = {}
    for row in postings:
        email = row[1].replace("@sfsu.edu", "")
        dPosting = {"email" : email , "title": row[2], "description":row[3], "date" : row[4], "price" : row[5], "image":row[7]}
        lst.append(dPosting)
    return lst




