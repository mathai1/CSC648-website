import pymysql
import datetime
from PIL import Image
from flask import session
class SearchingDB():
    def __init__(self):
        self.host = "csc648.cszroavxh2pu.us-west-2.rds.amazonaws.com"
        self.port = 3306
        self.dbname = "mydb"
        self.user = "root"
        self.password = "mypass123"
    def connect_db(self) :
        return pymysql.connect(host =self.host, user=self.user, port=self.port,passwd=self.password, db=self.dbname) 

    def createThumbnail(self, filepath,destination, width = 240, height = 240):
        image = Image.open(filepath)
        MAX_SIZE = (width, height)
        image.thumbnail(MAX_SIZE)
        image.save(destination)
    

###### retriving user info #############

# Method : Getting All User in the database
# Parameter : N/A
# Return : A list of tuple of user
# Option Return : If a return is a dict, call the method getOrganizedUser() to get a dict instead
    def getAllUsers(self):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = "SELECT * from User"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        return item

# Method : Matching email and password of user input to the User in database
# Parameter : email ( String) , password ( String )
# Return : A list of tuple of 1 user that matched email & passworkd
# Option Return : If a return is a dict, call the method getOrganizedUser() to get a dict instead

    def checkAUser(self, email , password):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = f"SELECT * from User WHERE email LIKE '{email}' AND password LIKE '{password}' "
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        return item

# Method : Get a particular user based on either firtName or lastName or email 
# Parameter : - First Parameter : Actual String of "firtName" or "lastName" or "email"
#             - Secomd parameter : Any String that either firstName or lastName or Email
# Return : A list of tuple of 1 user 
# Option Return : If a return is a dict, call the method getOrganizedUser() to get a dict instead

    def getAUser(self, catergory, searchedData):
        conn = self.connect_db()
        pycursor = conn.cursor()
        if catergory == "All" :
            searchQuery = f"SELECT * from User WHERE email LIKE '%{searchedData}%' OR firstName LIKE '%{searchedData}%' OR lastName LIKE '%{searchedData}%'"
        else :
            searchQuery = f"SELECT * from User WHERE {catergory} LIKE '%{searchedData}%'"
        data = pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        return item


# Method : Get a User by email
# Parameter : User email
# Return : A list of tuple of 1 user that matched email
# Option Return : If a return is a dict, call the method getOrganizedUser() to get a dict instead

    def getAUserbyEmail(self, email):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = f"SELECT * from User WHERE email LIKE '{email}' "
        data = pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        return item

# Method : Create a dictionary of User 
# Parameter : Tuple of users
# Return : A list of dictionary with key email , fname , lname , image

    def getUserOrganizedData(self,users) :
        lst = []
        dUsers = {}
        print(users)
        for row in users:
            # dUsers = {"email": row[0],  "fname":row[2], "lname":row[3], "image" : row[4]}
            dUsers = {"email": row[0],  "fname":row[2], "lname":row[3]}
            lst.append(dUsers)
        return lst

# Method : Insert a User in the database
# Parameter : A dictionary of a User with key email , password , fname , lname
# Return : N/A 

    def insertAUser(self, user):
        conn = self.connect_db()
        pycursor = conn.cursor()
        email = user['email']
        password = user['password']
        fname = user['fname']
        lname = user['lname']
        searchQuery = f"INSERT INTO User (email , password, firstName , lastName ) VALUES ('{email}' , '{password}' , '{fname}' ,  '{lname}'  )"
        data = pycursor.execute(searchQuery)
        conn.commit()
        conn.close()
        

###### retriving posting info #############

# Method : Get All Postings in the database
# Parameter : N/A
# Return : A list of tuple of tuple of posting
# Option Return : If want a return is a dict, call the method getOrganizedPosting() to get a dict instead
    
    def getAllPostings(self):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = "SELECT * from Posting"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()

        return item

# Method : Get Postings ordered by data
# Parameter : optional ascending or descending order
# Return : A list of tuple of tuple of posting

    def getPostingbyOrderedDate(self, ascending=False):
        conn = self.connect_db()
        pycursor = conn.cursor()
        if ascending:
            searchQuery = "SELECT * from Posting order by date ASC"
        searchQuery = "SELECT * from Posting order by date DESC"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()

        return item

# Method : Get A Posting with an exact match based on either "email" , "title", "description" , "date" , "price", "category"
# Parameter : - First Parameter : ACtual String of either "email" , "title", "description" , "date" , "price", "category"
#             - Second Parameter : A string that you want to search on post based on either "email" , "title", "description" , "date" , "price", "category"
# Return : A list of tuple of 1 tuple of all posting
# Option Return : If want a return is a dict, call the method getOrganizedPosting() to get a dict instead

    def getAPosting(self, category , posting):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = f"SELECT * from Posting WHERE {category} LIKE '{posting}' "
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()

        return item

# Method : This function is for searching a posting that includes a string from search input 
# Parameter : - First Parameter : ACtual String of either "All" , "book" or "misc" or "electronic"
#             - Second Parameter : A title string of Posting based on Catergory
# Return : A list of tuple of tuples of posting
# Option Return : If want a return is a dict, call the method getOrganizedPosting() to get a dict instead
    
    def searchAPosting(self, catergory, searchedData):
        conn = self.connect_db()
        pycursor = conn.cursor()
        if catergory == "All" :
            searchQuery = f"SELECT * from Posting WHERE title LIKE '%{searchedData}%' "
        else :
            searchQuery = f"SELECT * from Posting WHERE category LIKE '{catergory}' AND title LIKE '%{searchedData}%'"
        data = pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        return item

# Method : This function is for insert a post into a database
# Parameter : - A dictionary of posting with key "email" , "title", "description" , "date" , "price", "category"

    def insertAPosting(self, posting):
        conn = self.connect_db()
        pycursor = conn.cursor()
        email = session['email']
        title = posting['title']
        description = posting['description']
        price = posting['price']
        category = posting['category']
        image = posting['image']
        # image = "/images/postings/empty.png"

        searchQuery = f"INSERT INTO Posting (email ,title , description, price , category , image, date ) VALUES ('{email}' ,'{title}' , '{description}' , {price} ,  '{category}' ,  '{image}' , NOW() )"
        
        data = pycursor.execute(searchQuery)
        conn.commit()
        conn.close()

# Method : This function is A user based on Posting ID
# Parameter : posting id
# Return : A tuple of tuple of tuples of posting
# Option Return : If want a return is a dict, call the method getOrganizedPosting() to get a dict instead

    def getUserByPostingId(self,pid):
        conn = self.connect_db()
        pycursor = conn.cursor()
        
        searchQuery = f"SELECT U.firstName from Posting P, User U WHERE P.postID LIKE '{pid}'"
        data = pycursor.execute(searchQuery)
        user = pycursor.fetchone()[0]
        conn.close()
        print(user)
        return user

# Method : Create a dictionary of posting with key  "id" "email" , "title", "description" , "date" , "price", "category"
# Parameter : tuple of posting
# Return : A dict of posting

    def getPostingOrganizedData(self,postings) :
        lst = []
        dPosting = {}
        for row in postings:
            # email = row[1].replace("@sfsu.edu", "")
            email = row[1]

            date = row[4]
            if (type(date) == datetime.datetime):
                date = date.date()
            dPosting = {"postid" : row[0],"email" : email , "title": row[2], "description":row[3], "date" : date, "price" : row[5], "category": row[6], "image":row[7]}
            lst.append(dPosting)
        return lst

    def getPostingbyDate(self,searchData,category) :
        conn = self.connect_db()
        pycursor = conn.cursor()
        if category == "All" :
            searchQuery = f"SELECT * from Posting WHERE title LIKE '%{searchData}%' ORDER BY date ASC "
        else :
            searchQuery = f"SELECT * from Posting WHERE category LIKE '{category}' AND title LIKE '%{searchData}%' ORDER BY date ASC"
        data = pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        return item


# Method : Sorts by pricing AND date, defaults to newest to oldest
# Parameter : parameters from search page filter: min price, max price, order selection, search bar text, search bar category
# Return : A dict of postings

    def getPostingbyPrice(self, min, max, order, searchedData, category):
        conn = self.connect_db()
        pycursor = conn.cursor()
        if category == "All" :
            if order == "oldest" :
                searchQuery = f"SELECT * from Posting WHERE title LIKE '%{searchedData}%' AND price >= {min} AND price <= {max} order by DATE(date) DESC"
            else :
                searchQuery = f"SELECT * from Posting WHERE title LIKE '%{searchedData}%' AND price >= {min} AND price <= {max} order by DATE(date) ASC"
        else :
            if order == "oldest" :
                searchQuery = f"SELECT * from Posting WHERE category LIKE '{category}' AND title LIKE '%{searchedData}%' AND price >= {min} AND price <= {max} order by DATE(date) DESC"
            else:
                searchQuery = f"SELECT * from Posting WHERE category LIKE '{category}' AND title LIKE '%{searchedData}%' AND price >= {min} AND price <= {max} order by DATE(date) ASC"
        data = pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        item = self.getPostingOrganizedData(item)
        return item

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


############# Messages feature ###############

# Method : This function get all message handler based on author , inquiry and postID
# Parameter : author email , inquiry email , postID
# Return : A tuple of tuple of tuples of message handler 

    def generateMessageHandler(self, author,inquiry, postID):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = f"CALL first_message('{author}', '{inquiry}', {postID})"
        pycursor.execute(searchQuery)
        conn.commit()
        item = pycursor.fetchone()
        conn.close()
        return item

# Method : This function get all messages by a user 
# Parameter : user email
# Return : A tuple of tuple of tuples of posting
# Option Return : If want a return is a dict, call the method getMessageOrganizedData() to get a dict instead

    def getAllMessageByUser(self, user):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = f"SELECT * from Message_Handler WHERE author = '{user}' OR inquiry = '{user}'"
        pycursor.execute(searchQuery)
        conn.commit()
        item = pycursor.fetchall()
        item = self.getMessageOrganizedData(item)
        conn.close()
        return item

# Method : This function create a dictionary of message with key mhid , author , inquiry , postID 
# Parameter : message tuple
# Return : A dictionary of message

    def getMessageOrganizedData(self,message) :
        lst = []
        dMessage = {}
        for row in message:
            dMessage = {"mhid": row[0],  "author":row[1], "inquiry":row[2] , "postID":row[3] }
            lst.append(dMessage)
        return lst

# Method : This function insert a message into a database
# Parameter : message 
# Return : A tuple of tuple of tuples of posting
# Option Return : If want a return is a dict, call the method getOrganizedPosting() to get a dict instead

    def InsertMessage(self,message):
        conn = self.connect_db()
        pycursor = conn.cursor()
        body = message['body']
        mhid = message['room']
        sender = message['user']
        searchQuery = f"INSERT INTO Messages (Mhid, messagebody, sender, timestamp) VALUES ({mhid} , '{body}', '{sender}', NOW() ) "
        pycursor.execute(searchQuery)
        conn.commit()
        conn.close()

# Method : This function get all messaged based on message handler
# Parameter : message handler id
# Return : A tuple of tuple of tuples of messages

    def getAllMessagesByMessageHandler(self, mhid):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = f"SELECT * FROM Messages WHERE Mhid = {mhid}"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()

        item = self.getMessageBodyOrganizedData(item)
        conn.close()
        return item

    def getMessageBodyOrganizedData(self,message) :
        lst = []
        dMessage = {}
        for row in message:
            dMessage = {"mhid": row[1], "body":row[2] , "sender":row[3] }
            lst.append(dMessage)
        return lst


    #def getDashBoardMessage(self, message):
       # conn = self.connect_db()
        #pycursor = conn.cursor()
        #searchQuery = f"SELECT Posting.postID, Posting.email as Post_owner, Posting.title, Message_Handler.mhid, Message_Handler.inquiry, Messages.messagebody, Messages.timestamp FROM Posting JOIN Message_Handler on Message_Handler.postID = Posting.postID
#Join Messages on Message_Handler.mhid = Messages.mhid
#WHERE Posting.email = "b@sfsu.edu" or Message_Handler.inquiry = "b@sfsu.edu"
#GROUP BY(Message_Handler.mhid)
#Order by Messages.timestamp desc"
        #pycursor.execute(searchQuery)
        #item = pycursor.fetchall()

        #item = self.getMessageBodyOrganizedData(item)
        #conn.close()
        #return item


    






