# THIS IS HOME BLUEPRINT for home, about, login and signup
from flask import Blueprint, render_template,request,redirect,url_for,session
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

@home.route('/login',methods =['GET','POST'])
def login():
    alertmsg = ''

    if request.method == 'Submit' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        #Initing variables 
        username = request.form['username']
        password = request.form['password']
        email = request.form["email"]
    elif request.method == 'Submit':
        alertmsg = 'Please fill out the form!'
    return render_template("home/login.html", alertmsg=alertmsg)

@home.route('/signup')
def signup(name):
    return render_template("home/signup.html")

