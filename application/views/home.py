# THIS IS HOME BLUEPRINT for home, about, login and signup
from flask import Blueprint, render_template, request, session
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
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'pwd' in request.form:
        email=request.form['email']
        password=request.form['pwd']
        user=db.getAUser("email",email)
        if user:
            if email==user[0] and password==user[1]:
                session['loggedin']=True
                session['email']=user[0]
                session['firstname']=user[3]
                return redirect(url_for("home.homepage"))
        else:
            msg='Invalid Email/Password'
    return render_template("home/login.html", msg=msg)


@home.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = {}
        user['email'] = request.form['email']
        user['password'] = request.form['password']
        user['fname'] = request.form['fname']
        user['lname'] = request.form['lname']
        db.insertAUser(user)
        return render_template("home/login.html" , message = "Account is created")
    return render_template("home/signup.html")

<<<<<<< HEAD
@home.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('email',None)
    session.pop('firstname',None)
    return redirect(url_for("home.homepage"))



=======
>>>>>>> dangbranch

