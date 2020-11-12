# THIS IS Posting BLUEPRINT for posting page
#retriveing a posting 
# /posting/<postingid>
from flask import Blueprint, render_template, request
from db import SearchingDB
db = SearchingDB()

posting = Blueprint('posting', __name__)

@posting.route('/posting/<postid>')
def getPost(postid):
    post = db.getAPosting("postID", postid)
    posts = db.getPostingOrganizedData(post)
    return render_template("posting/posting.html", posting = posts[0] )

@posting.route('/posting')
def createPost():
    return render_template("posting/create.html")