# THIS IS Posting BLUEPRINT for posting page
#retriveing a posting 
# /posting/<postingid>
from flask import Blueprint, render_template, request
from db import SearchingDB
db = SearchingDB()

posting = Blueprint('posting', __name__)


@posting.route('/posting')
def post():
    return render_template("posting/posting.html")


@posting.route('/posting/<title>')
def getPost(title):
    page = "posting/posting.html"
    postings = db.searchAPosting("All",title)
    lst = db.getPostingOrganizedData(postings)
    return render_template(page, posting = lst[0])