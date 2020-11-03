# THIS IS search BLUEPRINT for search result page
from flask import Blueprint, render_template, request
from db import SearchingDB
db = SearchingDB()

search = Blueprint('search', __name__)

@search.route('/search', methods= ['GET' , 'POST'])
def searchpage():
    if request.method == 'POST':
        category =request.form['filter']
        searchedData =request.form['searchedData']
        postings = db.searchAPosting(category,searchedData)
        lst = db.getPostingOrganizedData(postings)
        return render_template("search/search.html", data = lst)
    return render_template("search/search.html")

