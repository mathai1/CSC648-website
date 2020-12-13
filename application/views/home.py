# THIS IS HOME BLUEPRINT for home, about, login and signup
from flask import Blueprint, render_template, request, session, redirect, url_for
import re

def initHome(db):
    # create a blue print
    home = Blueprint('home', __name__)

    @home.route('/', methods=['GET'])
    def homepage():
        # Getting posting info from the database
        postings = db.getAllPostings()
        lst = db.getPostingOrganizedData(postings)
        recent_posts = db.getPostingbyOrderedDate()
        ordered_lst = db.getPostingOrganizedData(recent_posts)
        numberOfPostings = int(len(ordered_lst))

        #Geting thumbnail
        ordered_lst = getThumbnail(ordered_lst)
        lst = getThumbnail(lst)
        
        #Getting book posting info
        books = db.getBookPostings()
        book_postings = db.getPostingOrganizedData(books)
        book_postings = getThumbnail(book_postings)
        bookCount = int(len(book_postings))

            
        #print(books)

        # display favorite when user favorite something
        if 'name' in session:
            user = db.getAUser("All",session['name'])
            favorites = db.getfavoritePostings(session['email'])
            fav_postings = db.getPostingOrganizedData(favorites)
            fav_postings = getThumbnail(fav_postings)
            return render_template('home/home.html', data = lst, bookData=book_postings, recent = ordered_lst, fav = fav_postings,
             user=user, numberOfPostings=numberOfPostings, bookCount=bookCount)

        return render_template('home/home.html', data = lst, bookData=book_postings, recent = ordered_lst, numberOfPostings=numberOfPostings, bookCount=bookCount)
        
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
            password =request.form['pwd']
            account = db.checkAUser(email,password)
            if account :
                session['email'] = request.form['email']
                user = db.getUserOrganizedData(account)
                session['name'] = user[0]['fname']
                return redirect(url_for('home.homepage'))
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

    def getThumbnail(lst) :
        for l in lst:
            s = l['image'].split("/")[-1]
            l['image'] = "media/" + s 
        return lst

    return home




