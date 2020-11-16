######################################################################################
# THIS IS HOME BLUEPRINT for message
######################################################################################

from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_socketio import emit, join_room, leave_room

def initChat(db, socketio):
# create a blue print
    message = Blueprint('message', __name__)

    @message.route('/message', methods=['GET','POST'])
    def messageRoute():
        # if 'author' in request.args and 'postID' in request.args:
        #     inquiry = session['email']
        #     author = request.args['author']
        #     postID = request.args['postID']
        #     data = db.generateMessageHandler(author, inquiry, postID)
            return redirect(f'/message/1')
            
    @message.route('/message/<id>', methods= ['GET' , 'POST'])
    def Messagepage(id):
        user = session['name']
        message = db.getAllMessagesByMessageHandler(id)
        return render_template('message/chat.html', async_mode=socketio.async_mode, data=id, user = user, messages = message)
            

    @socketio.on('join', namespace='/test')
    def join(message):
        join_room(message['room'])


    @socketio.on('my_room_event', namespace='/test')
    def send_room_message(message):
        print(message)
        # db.InsertMessage(message)
        emit('my_response',
            {'data': message['data'], 'user': message['user']},
            room=message['room'])

    return message