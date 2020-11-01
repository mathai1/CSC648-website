# File structure
```
application/
    README.md
    app.py
    db.py
    templates/
        base.html
        dashboard/
            message.html
            postings.html
        home/
            about.html
            home.html
            login.html
            signup.html
            about/
        posting/
            posting.html
        profile/
        search/
            search.html
    static/
        css/
        images/
    tests/
    views/
        __init__.py
        dashboard.py
        home.py
        posting.py
        profile.py
        search.py
```
Using blue print to structure the file for this project.
Blueprint is the collection of views , static file and template.
In this application, the structure is divided  by its function.
The blueprint in views folder collections of views.
The same static files will be used for the views in most of the blueprints.
Most of the templates will extend a master template.
Each of the python file in views folder is basically a blueprint . These blueprint will have the 
template folder corresponsing with its name
For example: home.py has home folder in template

# Application Folder

## Purpose
The purpose of this folder is to store all the source code and related files for your team's application. Source code MUST NOT be in any of folder. <strong>YOU HAVE BEEN WARNED</strong>

You are free to organize the contents of the folder as you see fit. But remember your team is graded on how you use Git. This does include the structure of your application. Points will be deducted from poorly structured application folders.

## Please use the rest of the README.md to store important information for your team's application.

## SET UP
### Create an environment 
Windows
```
$ py -3 -m venv venv
```
Mac
```
python3 -m venv venv
```
### Activate the environment 
Windows
```
> venv\Scripts\activate
```
Mac
```
$ . venv/bin/activate
```

# Install the dependencies
```
pip3 install -r requirements.txt

```
# Run nginx 

```
sudo nginx 

```
# Run the Flask application 
```
$ gunicorn app:app
```


## Flask application 

# Routing 
In the website , we are usually see something like www.facebook.com . The .com is the domain name. When this link to domain server find the name facebook and will response back to you a html file of a default home /
Same with  www.facebook.com/<username> , will reponse back to you a html page of user name /<username>
In our flask application , this handle to find a correct html file that a user request , and then reponse back with the html

This is the syntax : 

```    
@app.route('/something')
def something(): // 
    return render_template("something.html")
```
@app.route('/something') is the syntax of the route in the website
then we return back the html file by using  return render_template("something.html")

======> Just replace something with the route you want to route, remember to have the html file 
# Database
## Connection to the database
We have all the database code in db.py. We will need to import pymysql. This module handle as a middleware to connect our flask application to mysql
```
    def connect_db(self) :
        return pymysql.connect(host =self.host, user=self.user, port=self.port,passwd=self.password, db=self.dbname) 
```

## Using the database
We have a this of code block as connect, retrive the information/data and then close the the db connection and return the item

```
    def getAllUsers(self):
        conn = self.connect_db() // This is a function above to connect with the database
        pycursor = conn.cursor() // this is a cursor act as a pointer and point to the beginning of the db
        searchQuery = "SELECT * from User" // Any query that you want to the cursor
        pycursor.execute(searchQuery) // When we have the cursor on top of the db, we can execute the query
        item = pycursor.fetchall() // The fetchAll function will get all the row that matches the query in the db
        conn.close() // We need to close the connection to reset the cursor pointer back to the top of the db
        return item
```
With this codeblock you can do anything with the database followed the code above, The only change is the query in search query

## Database tables
This is inside the mysql workbench. You can add/ remove data or table using the  mysql workbench
In our case. I created a table Users  . 
These are the sample data 
-- --------------------------------------
email          | password | firstName | lastName
--- -------------------------------------
dnguyen49@mail |  123     | -----     |
---- ------------------------------------
banana@mail     |   123    |   ------  |
----- -----------------------------------
apple@mail      | 123      | -------   |


# Searching architecture
## Frontend ( html file)
This is a code block for the search box in the html 
```
      <form class="form-inline my-2 my-lg-0" action ="/search" method ="POST">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Catergory
          </a>
            <select class="dropdown-menu" aria-labelledby="navbarDropdown" name="filter" >
              <option class="dropdown-item" value ="All" >All</option>
              <option class="dropdown-item" value ="email" >email</option>
              <option class="dropdown-item" value ="firstName">first Name</option>
              <option class="dropdown-item" value = "lastName">last name</option>

            </select>
        </li>
```

The code block need to be a form atribute , a POST method and need to have a action
A POST method allow the user to send a data to the server. In this case is what they type in the search box

```
<form class="form-inline my-2 my-lg-0" action ="/search" method ="POST">
```
In each option that we have a value = " nameofValue " . The nameofValue will match with the name in the databae
```
<option class="dropdown-item" value ="All" >All</option>
<option class="dropdown-item" value ="email" >email</option>
<option class="dropdown-item" value ="firstName">first Name</option>
<option class="dropdown-item" value = "lastName">last name</option>
```

## Connect front end and backend
In app.py 
```
from db import SFSU_DB
db = SFSU_DB()
```
In db.py we have a class to do evrything related to the db

```
@app.route('/search', methods= ['GET' , 'POST'])
def search():
    if request.method == 'POST':
        category =request.form['filter']
        searchedData =request.form['searchedData']
        users = db.getAUser(category,searchedData)
        lst = getOrganizedData(users)
        return render_template("search.html", data = lst)
    return render_template("search.html")
```

When the user type somthing, it send the data through POST . Remember this line in the frontend ? 
```
      <form class="form-inline my-2 my-lg-0" action ="/search" method ="POST">
```

To get the data , we use request.form 
```
request.form
```
In our case we have filter and searchedData in our form . This need to be matched with the name in our html file

....
We have the db and we have the data from the users. Now to use it , and search the data through our database, everything is defined inside the function getAUser 

```
users = db.getAUser(category,searchedData)
```

Once you retrived data from the datase . I organize this data to a dictionary. This help easier to display back to the front end
```
lst = getOrganizedData(users)
```
And render the template html file with the lst . And I save lst to data variable
```
return render_template("search.html", data = lst)
```

This is how to display to the frontend in search.html:
Flask makes it easier to use if else in side html 
```
{% extends "base.html" %}
{% block title%}test search{% endblock %}
{% block content %}  
  <div>
    {%if data %}
    {% for d in data %}
      <ul> 
        {{d["email"]}}  {{d["fname"]}}  {{d["lname"]}}
      </ul>  
    {% endfor %}
    {% endif %}
  </div>
{% endblock %}
```












