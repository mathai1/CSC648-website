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

#     def getDashBoardMessage(self, message):
#         conn = self.connect_db()
#         pycursor = conn.cursor()
#         searchQuery = f"SELECT Posting.postID, Posting.email as Post_owner, Posting.title, Message_Handler.mhid, Message_Handler.inquiry, Messages.messagebody, Messages.timestamp FROM Posting JOIN Message_Handler on Message_Handler.postID = Posting.postID
# Join Messages on Message_Handler.mhid = Messages.mhid
# WHERE Posting.email = "b@sfsu.edu" or Message_Handler.inquiry = "b@sfsu.edu"
# GROUP BY(Message_Handler.mhid)
# Order by Messages.timestamp desc"
#         pycursor.execute(searchQuery)
#         item = pycursor.fetchall()

#         item = self.getMessageBodyOrganizedData(item)
#         conn.close()
#         return item
