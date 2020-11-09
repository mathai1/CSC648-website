# THIS IS dashboard BLUEPRINT for dashboard page
# This is where user their dashboard for postings or messages
from flask import Blueprint, render_template, request
from db import SearchingDB
db = SearchingDB()

dashboard = Blueprint('dashboard', __name__)

# @dashboard.route('/user/<username>')
# @login_required
# def user(username):
#     user = db.user.query.filter_by(username=username).first_or_404()
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}
#     ]
#     return render_template('dashboard.html', user=user, posts=posts)



@dashboard.route('/messages')
def messages():
    msgs = [
        {
            'postTitle': 'Book1',
            'postPrice': 70.00,
            'timestamp': 'Dec 12 2020 14:43:04',
            'otherUser': 'John Appleseed',
            'lastMessage': 'This is an example of the last message that was sent in the conversation.'
        },
        {
            'postTitle': 'Book2',
            'postPrice': 12.00,
            'timestamp': 'Feb 01 2020 15:28:12',
            'otherUser': 'John Doe',
            'lastMessage': 'This is an example of the last message that was sent in the conversation.'
        },
        {
            'postTitle': 'Book3',
            'postPrice': 4.00,
            'timestamp': 'Dec 12 2020 02:32:39',
            'otherUser': 'Jane Doe',
            'lastMessage': 'This is an example of the last message that was sent in the conversation.'
        },
        {
            'postTitle': 'Book4',
            'postPrice': 23.00,
            'timestamp': 'Dec 12 2020 18:14:59',
            'otherUser': 'Joe Momma',
            'lastMessage': 'This is an example of the last message that was sent in the conversation.'
        },
    ]
    numMsgs = len(msgs)
    return render_template('dashboard/message.html', msgs=msgs, numMsgs=numMsgs)

@dashboard.route('/userPostings')
def userPostings():
    allPosts = db.getAllPostings()
    posts = db.getPostingOrganizedData(allPosts)
    numPosts = len(posts)
    return render_template('dashboard/postings.html', posts=posts, numPosts=numPosts)