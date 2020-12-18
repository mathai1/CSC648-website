import pymysql
import datetime, bcrypt
from PIL import Image
from flask import session
class User():
    def __init__(self, host, user, port, password, dbname ):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
    def connect_db(self) :
        return pymysql.connect(host =self.host, user=self.user, port=self.port,passwd=self.password, db=self.dbname) 


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
        searchQuery = f"SELECT * from User WHERE email LIKE '{email}' "
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
            dUsers = {"email": row[0],"password" : row[1] , "fname":row[2], "lname":row[3]}
            lst.append(dUsers)
        return lst

# Method : Insert a User in the database
# Parameter : A dictionary of a User with key email , password , fname , lname
# Return : N/A 

    def insertAUser(self, user):
        conn = self.connect_db()
        pycursor = conn.cursor()
        email = user['email']
        email = email.replace("'" ,"\\'")
        password = user['password']
        password = password.replace("'" ,"\\'")
        fname = user['fname']
        fname = fname.replace("'" ,"\\'")
        lname = user['lname']
        lname = lname.replace("'" ,"\\'")
        searchQuery = f"INSERT INTO User (email , password, firstName , lastName ) VALUES ('{email}' , '{password}' , '{fname}' ,  '{lname}'  )"
        data = pycursor.execute(searchQuery)
        conn.commit()
        conn.close()
        

