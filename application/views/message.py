######################################################################################
# THIS IS HOME BLUEPRINT for message
######################################################################################

from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_socketio import emit, join_room, leave_room

def initChat(db, socketio):
# create a blue print
    message = Blueprint('message', __name__)

    @message.route('/message', methods=['GET','POST'])
    def CreateMessageRoute():
        if 'author' in request.args and 'postID' in request.args:
            inquiry = session['email']
            author = request.args['author']
            postID = int(request.args['postID'])
            data = db.message.generateMessageHandler(author, inquiry, postID)
            return redirect(f'/message/{data[0]}')
            
    @message.route('/message/<id>', methods= ['GET' , 'POST'])
    def Messagepage(id):
        user = session['name']
        message = db.message.getAllMessagesByMessageHandler(id)
        print(message)
        return render_template('message/message.html', id=id, user = user, messages = message)

    # @message.route('/messages', methods= ['GET' , 'POST'])
    # def MessagebyUserpage(id):
    #     user = session['name']
    #     message = db.message.getDashBoardMessage()
    #     print(message)
    #     return render_template('message/message.html', id=id, user = user, messages = message)
            

    @message.route('/message/<id>/send', methods= ['GET' , 'POST'])
    def send_room_message(id):
        if request.method == "POST" :
            messages ={}
            messages['body'] = request.form['message']
            messages['room'] = id 
            messages['user'] = session['email']
            db.message.InsertMessage(messages)
        data = db.message.getAllMessagesByMessageHandler(id)
        # return render_template('message/message.html', id=id, user =session['name'] , messages = data)
        return redirect(f"/message/{id}")


    return message