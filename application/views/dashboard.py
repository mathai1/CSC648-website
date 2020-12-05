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
        # msgs = [
        #     {
        #         'postTitle': 'Book1',
        #         'postPrice': 70.00,
        #         'timestamp': 'Dec 12 2020 14:43:04',
        #         'otherUser': 'John Appleseed',
        #         'lastMessage': 'This is an example of the last message that was sent in the conversation.'
        #     },
        #     {
        #         'postTitle': 'Book2',
        #         'postPrice': 12.00,
        #         'timestamp': 'Feb 01 2020 15:28:12',
        #         'otherUser': 'John Doe',
        #         'lastMessage': 'This is an example of the last message that was sent in the conversation.'
        #     },
        #     {
        #         'postTitle': 'Book3',
        #         'postPrice': 4.00,
        #         'timestamp': 'Dec 12 2020 02:32:39',
        #         'otherUser': 'Jane Doe',
        #         'lastMessage': 'This is an example of the last message that was sent in the conversation.'
        #     },
        #     {
        #         'postTitle': 'Book4',
        #         'postPrice': 23.00,
        #         'timestamp': 'Dec 12 2020 18:14:59',
        #         'otherUser': 'Joe Momma',
        #         'lastMessage': 'This is an example of the last message that was sent in the conversation.'
        #     },
        # ]
        msgs = db.message.getDashBoardMessage()
        print(msgs)
        numMsgs = len(msgs)
        return render_template('dashboard/message.html', msgs=msgs, numMsgs=numMsgs)

    @dashboard.route('/userPostings')
    def userPostings():
        # allPosts = db.getAllPostings()
        # posts = db.getPostingOrganizedData(allPosts)
        allPosts = db.post.getAPosting("email", session['email'])
        posts = db.post.getPostingOrganizedData(allPosts)
        numPosts = len(posts)
        return render_template('dashboard/postings.html', posts=posts, numPosts=numPosts)
        
    return dashboard