from flask import Flask, render_template
import pymysql
app = Flask(__name__)

host = "csc648.cszroavxh2pu.us-west-2.rds.amazonaws.com"
port = 3306
dbname = "mydb"
user = "root"
password = "mypass123"

conn = pymysql.connect(host =host, user=user, port=port,passwd=password, db=dbname) 
pycursor = conn.cursor()
searchQuery = "SELECT * from users"
data = pycursor.execute(searchQuery)
item = pycursor.fetchone()
print(item)
conn.close()

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/search')
def search():
    return render_template("search.html")
    
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/about/<name>')
def getPerson(name):
    item = f"{name}.html"
    return render_template(item, name = name)
