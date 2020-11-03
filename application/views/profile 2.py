# THIS IS profile BLUEPRINT for profile page
# This is where user can see their own profile
#They can view/ edit it
from flask import Blueprint, render_template, request
from db import SearchingDB
db = SearchingDB()

profile = Blueprint('profile', __name__)