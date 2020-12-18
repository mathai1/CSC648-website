import pymysql
import datetime
from PIL import Image
from flask import session
class Post():
    def __init__(self, host, user, port, password, dbname ):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
    def connect_db(self) :
        return pymysql.connect(host =self.host, user=self.user, port=self.port,passwd=self.password, db=self.dbname) 
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
        title = title.replace("'" ,"\\'")
        description = posting['description']
        description = description.replace("'" ,"\\'")
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

    def getPostingOrganizedData(self,postings,approve=1) :
        lst = []
        dPosting = {}
        for row in postings:
            # email = row[1].replace("@sfsu.edu", "")
            email = row[1]

            date = row[4]
            if (type(date) == datetime.datetime):
                date = date.date()
            if approve == row[8] :
                dPosting = {"postid" : row[0],"email" : email , "title": row[2], "description":row[3], "date" : date, "price" : row[5], "category": row[6], "image":row[7], "approve" : row[8]}
                lst.append(dPosting)
            elif approve == 2 :
                dPosting = {"postid" : row[0],"email" : email , "title": row[2], "description":row[3], "date" : date, "price" : row[5], "category": row[6], "image":row[7], "approve" : row[8]}
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


    def getBookPostings(self):
        conn = self.connect_db()
        pycursor = conn.cursor()
        searchQuery = "select * from Posting where category = 'Books' AND approval = 1"
        pycursor.execute(searchQuery)
        item = pycursor.fetchall()        
        conn.close()

        return item

# Method : Sorts by pricing AND date AND category
# Parameter : parameters from search page filter: order selection, search bar text, search bar category
# Return : A dict of postings

    def getPostingbyDateAndFilter(self, order, searchData, category) :
        conn = self.connect_db()
        pycursor = conn.cursor()
        if category == "All" :
            if order == "newest":
                searchQuery = f"SELECT * from Posting WHERE title LIKE '%{searchData}%' AND approval = 1 ORDER BY date DESC"
            else:
                searchQuery = f"SELECT * from Posting WHERE title LIKE '%{searchData}%' AND approval = 1 ORDER BY date ASC"
        else :
            if order == "newest":
                searchQuery = f"SELECT * from Posting WHERE category LIKE '{category}' AND title LIKE '%{searchData}%' AND approval = 1 ORDER BY date DESC"
            else:
                searchQuery = f"SELECT * from Posting WHERE category LIKE '{category}' AND title LIKE '%{searchData}%' AND approval = 1 ORDER BY date ASC"

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

# Method: this function deletes a post from a logged in user
# Parameter: post id
# Return: nothing

    def deleteAPosting(self, postId):
        conn = self.connect_db()
        pycursor = conn.cursor()
        deleteQuery = f"DELETE from Posting WHERE postID={postId}"
        pycursor.execute(deleteQuery)
        conn.commit()
        conn.close()