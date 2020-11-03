import pymysql

class SearchingDB():
    def __init__(self):
        self.host = "csc648.cszroavxh2pu.us-west-2.rds.amazonaws.com"
        self.port = 3306
        self.dbname = "mydb"
        self.user = "root"
        self.password = "mypass123"
    def connect_db(self) :
        return pymysql.connect(host =self.host, user=self.user, port=self.port,passwd=self.password, db=self.dbname) 

    def getAllUsers(self):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = "SELECT * from User"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()
        return item
        
    def getAUser(self, category, searchedData):
        conn = self.connect_db()
        pycursor = conn.cursor()
        if category == "All" :
            searchQuery = f"SELECT * FROM User WHERE email LIKE '%{searchedData}%' "
        else :
            searchQuery = f"SELECT * FROM User WHERE {category} LIKE '%{searchedData}%'"
        pycursor.execute(searchQuery)
        item = pycursor.fetchone()
        conn.close()
        return item

    
    def getAllPostings(self):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = "SELECT * from Posting"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()
        conn.close()

        return item

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
    
    def getUserOrganizedData(self,users) :
        lst = []
        dUsers = {}
        for row in users:
            dUsers = {"email": row[0], "password":row[1], "fname":row[2], "lname":row[3], "image" : row[4]}
            lst.append(dUsers)
        return lst

    def getPostingOrganizedData(self,postings) :
        lst = []
        dPosting = {}
        for row in postings:
            email = row[1].replace("@sfsu.edu", "")
            dPosting = {"email" : email , "title": row[2], "description":row[3], "date" : row[4], "price" : row[5], "image":row[7]}
            lst.append(dPosting)
        return lst
"""
    def getUserLoginInfo(self, user):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = "SELECT * FROM accounts WHERE '{username}' AND '{password}', (username, password,)"
        data = pycursor.execute(searchQuery)
        account = pycursor.fetchall()
        
        alertmsg = ''
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            return 'Logged in successfully!'
        
        else:
            alertmsg = 'Incorrect username or password!'
        conn.close()
        return account
    """

