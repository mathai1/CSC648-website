import pymysql
import datetime
from PIL import Image
from flask import session
from .user import User
from .post import Post
from .message import Message

class SearchingDB():
    def __init__(self):
        self.host = "csc648.cszroavxh2pu.us-west-2.rds.amazonaws.com"
        self.port = 3306
        self.dbname = "mydb"
        self.userName = "root"
        self.password = "mypass123"
        self.user = User(self.host, self.userName, self.port, self.password,  self.dbname )
        self.post = Post(self.host, self.userName, self.port, self.password,  self.dbname )
        self.message = Message(self.host, self.userName, self.port, self.password,  self.dbname )
    def connect_db(self) :
        return pymysql.connect(host =self.host, user=self.userName, port=self.port,passwd=self.password, db=self.dbname) 

    def createThumbnail(self, filepath,destination, width = 240, height = 240):
        image = Image.open(filepath)
        MAX_SIZE = (width, height)
        image.thumbnail(MAX_SIZE)
        image.save(destination)
    


############# Favorites feature #################
# Method : This function adding a post into a favorite table
# Parameter : postid and useremail
# Return : N/A 

    def addFavorite(self, postID, user):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = f"INSERT INTO favorites (postID , email) VALUES ({postID} , '{email}')"
        data = pycursor.execute(searchQuery)
        conn.commit()
        conn.close()

# Method : This function get all posting that is user's favorite
# Parameter : user email
# Return : A tuple of tuple of tuples of posting
# Option Return : If want a return is a dict, call the method getOrganizedPosting() to get a dict instead

    def getfavoritePostings(self,user):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = f"SELECT Posting.* FROM favorites Join Posting on favorites.postID=Posting.postID WHERE favorites.email = '{user}'"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        return item

############# Categories feature ###############

# Method : This function get all categories name in the database
# Parameter : N/ A
# Return : A tuple of tuple of tuples of catergory name

    def getCategories(self):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = "SELECT * from Category"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        return item


    






