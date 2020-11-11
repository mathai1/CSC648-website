# THIS IS Posting BLUEPRINT for posting page
#retriveing a posting 
# /posting/<postingid>
from flask import Blueprint, render_template, request
from db import SearchingDB
db = SearchingDB()

posting = Blueprint('posting', __name__)
