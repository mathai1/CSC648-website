# THIS IS HOME BLUEPRINT for home, about, login and signup
from flask import Blueprint, render_template
from db import SearchingDB
db = SearchingDB()

# create a blue print
home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def homepage():
    postings = db.getAllPostings()
    lst = db.getPostingOrganizedData(postings)
    return render_template('home/home.html', data = lst)
@home.route('/about')
def about():
    return render_template("home/about.html")

@home.route('/about/<name>')
def getPerson(name):
    item = f"home/about/{name}.html"
    return render_template(item, name = name)

@home.route('/login')
def login():
    return render_template("home/login.html")

@home.route('/signup')
def signup(name):
    return render_template("home/signup.html")

