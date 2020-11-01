# THIS IS dashboard BLUEPRINT for dashboard page
# This is where user their dashboard for postings or messages
from flask import Blueprint, render_template, request
from db import SearchingDB
db = SearchingDB()

dashboard = Blueprint('dashboard', __name__)
