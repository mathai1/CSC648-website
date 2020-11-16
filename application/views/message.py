# THIS IS HOME BLUEPRINT for message
from flask import Blueprint, render_template, request, session, redirect, url_for
# from db import SearchingDB

# db = SearchingDB()

def initChat(db):
# create a blue print
    message = Blueprint('message', __name__)

    @message.route('/chat')
    def chatpage():
        return render_template("message/chat.html")
    return message