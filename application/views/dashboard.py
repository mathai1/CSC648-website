# THIS IS dashboard BLUEPRINT for dashboard page
# This is where user their dashboard for postings or messages
from flask import Blueprint, render_template, request,session


def initDashBoard(db):
    dashboard = Blueprint('dashboard', __name__)

    @dashboard.route('/dashboard')
    def dashboardPage():
        return render_template('dashboard/dashboard.html')

    @dashboard.route('/messages')
    def messages():
        msgs = db.message.getDashBoardMessage()
        print(msgs)
        numMsgs = len(msgs)
        return render_template('dashboard/message.html', msgs=msgs, numMsgs=numMsgs)

    @dashboard.route('/userPostings')
    def userPostings():
        # allPosts = db.getAllPostings()
        # posts = db.getPostingOrganizedData(allPosts)
        allPosts = db.post.getAPosting("email", session['email'])
        posts = db.post.getPostingOrganizedData(allPosts,2)
        numPosts = len(posts)
        return render_template('dashboard/postings.html', posts=posts, numPosts=numPosts)

    @dashboard.route('/dashboard/delete/<postid>', methods= ['GET' , 'POST'])
    def deletePost(postid):
        print(postid)
        db.post.deleteAPosting(postid)

        #getting all the remaining posts in current account
        allPosts = db.post.getAPosting("email", session['email'])
        posts = db.post.getPostingOrganizedData(allPosts)
        numPosts = len(posts)

        return render_template('dashboard/postings.html', posts=posts, numPosts=numPosts)
        
    return dashboard