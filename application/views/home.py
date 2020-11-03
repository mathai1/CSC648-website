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
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'pwd' in request.form:
        email=request.form['email']
        password=request.form['pwd']
        user=db.getAUser("email",email)
        if user:
            if email==user[0] and password==user[1]:
                return render_template("home/home.html")
        else:
            msg='Invalid Email/Password'
        
    return render_template("home/login.html", msg=msg)

@home.route('/signup')
def signup(name):
    return render_template("home/signup.html")

@home.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('email',None)
    return render_template("home.html")




