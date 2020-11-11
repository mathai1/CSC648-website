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
    if 'loggedin' in session:
        return render_template('home/home.html', data = lst, user=session['firstname'])
    return render_template('home/home.html', data = lst)
    
@home.route('/about')
def about():
    if 'loggedin' in session:
        return render_template("home/about.html",user=session['firstname'])
    return render_template("home/about.html")

@home.route('/about/<name>')
def getPerson(name):
    item = f"home/about/{name}.html"
    if 'loggedin' in session:
        return render_template(item, name = name,user=session['firstname'])
    return render_template(item, name = name)

@home.route('/login/',methods =['GET','POST'])
def login():
    #initializing variable for Error Message
    msg = ''
    #If items are inputted by user
    if request.method == 'POST' and 'email' in request.form and 'pwd' in request.form:
        #retrieves inputs from users
        email=request.form['email']
        password=request.form['pwd']
        #find user data from database 
        user=db.getAUser("email",email)
        #if user found in database
        if user:
            if email==user[0] and password==user[1]:
                session['loggedin']=True
                session['email']=user[0]
                session['firstname']=user[3]
                return redirect(url_for("home.homepage"))
        #else return error message
        else:
            msg='Invalid Email/Password'
    #if no input then bring up an empty login page
    return render_template("home/login.html", msg=msg)


@home.route('/signup')
def signup(name):
    return render_template("home/signup.html")

@home.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('email',None)
    session.pop('firstname',None)
    return redirect(url_for("home.homepage"))




