# THIS IS HOME BLUEPRINT for home, about, login and signup
from flask import Blueprint, render_template, request, session, redirect, url_for
import re
# from db import SearchingDB

# db = SearchingDB()

def initHome(db):
# create a blue print
    home = Blueprint('home', __name__)

    @home.route('/', methods=['GET'])
    def homepage():
        postings = db.getAllPostings()
        lst = db.getPostingOrganizedData(postings)
        for l in lst:
            s = l['image'].split("/")[-1]
            l['image'] = "media/" + s 
        # if 'loggedin' in session:
        #     return render_template('home/home.html', data = lst, user=session['firstname'])
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

    @home.route('/login',methods =['GET','POST'])
    def login():
        if request.method == 'POST':
            email =request.form['email']
            password =request.form['password']
            account = db.checkAUser(email,password)
            if account :
                # session['loggedin'] = True
                session['email'] = request.form['email']
                user = db.getUserOrganizedData(account)
                session['name'] = user[0]['fname']
                postings = db.getAllPostings()
                postinglst = db.getPostingOrganizedData(postings)
                return render_template("home/home.html", data = postinglst, user = user)
            else :
                return render_template("home/login.html", message = "email or password is incorrect")
        return render_template("home/login.html")

    @home.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            message=""
            user = {}
            email = request.form['email']
            password = request.form['password']
            fname = request.form['fname']
            lname = request.form['lname']
            #checking whether email is a sfsu email or a email in database
            if "sfsu.edu" in email:
                user['email'] = email
            else:
                message = "Not SFSU Email"
            #checking whether the email has been rgistered already
            if db.getAUserbyEmail(email):
                message = "The email has been already registered"
            #checking if password contains at least 7 characters, 1 number, and 1 letter
            if len(password) < 7:
                message = "Password must have at least 7 characters" 
            elif re.search('[0-9]',password) is None:
                message ="Password must include a number"
            elif re.search('[a-z]',password) is None:
                message ="Password must include a letter"
            else:
                user['password']=password     
            #checking if name is only letters
            if fname.isalpha() & lname.isalpha():
                user['fname'] = fname
                user['lname'] = lname
            else:
                message = "First name and Last Name can only contain letters"
            #if there is no errors or messages on signup page
            #then insert user to database
            if not message:
                db.insertAUser(user)
                return render_template("home/login.html" , msg = "Account is created")
            else:
                return render_template("home/signup.html", message = message)
        return render_template("home/signup.html")

    @home.route('/logout')
    def logout():
        session.pop('email',None)
        session.pop('name',None)
        return redirect(url_for("home.homepage"))

    return home




