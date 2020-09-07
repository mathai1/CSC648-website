from application import app
from flask import render_template

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/about/dang')
def dang_profile():
    return render_template('/profile/dang.html')