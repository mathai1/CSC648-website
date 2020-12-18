import pymysql
import datetime
from PIL import Image
from flask import session
class Message():
    def __init__(self, host, user, port, password, dbname ):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
    def connect_db(self) :
        return pymysql.connect(host =self.host, user=self.user, port=self.port,passwd=self.password, db=self.dbname) 
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
        body = body.replace("'" ,"\\'")
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

    def getDashBoardMessage(self ):
        conn = self.connect_db()
        pycursor = conn.cursor()
        email = session['email']
        searchQuery = f"Call getLastMessage('{email}')"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()

        lst = []
        dMessage = {}
        for row in item:
            dMessage =  { "mhid" : row[1] , "body":row[2] , "sender":row[3], "timestamp": row[4], "postId": row[7], "postOwner" : row[8], "postTitle" : row[9] }
            lst.append(dMessage)        
        conn.close()
        return lst
