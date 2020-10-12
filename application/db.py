import pymysql

class SFSU_DB():
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





