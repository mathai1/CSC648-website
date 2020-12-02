#Using blue print to structure the file
#Blueprint is the collection of views , static file and template
#In this application, the structure is divided  by its function
#The blueprint in views folder collections of views
#The same static files will be used for the views in most of the blueprints
# Most of the templates will extend a master template

from flask import Flask
from flask_thumbnails import Thumbnail
from views.search import initSearch
from views.home import initHome
from views.posting import initPost
from views.dashboard import initDashBoard
from views.profile import profile
from views.message import initChat

from datetime import timedelta
from db import SearchingDB
from flask import send_from_directory

from flask_socketio import SocketIO


socket_io = SocketIO()

#Initialize flask app
app = Flask(__name__)


# Setting app session
app.permanent_session_lifetime=timedelta(days=1)

#Initialize db
db = SearchingDB()


#db.createThumbnail("static/images/postings/empty.png" , "static/media/empty.png", 240 , 240)
# Setting jinga global
@app.context_processor
def init():
    cat = db.getCategories() # Getting categories from database and make it glbal for navbar
    return dict(navlst = cat)

# Setting key for session
app.secret_key="GATOR"

# Passing db to all the blueprints & get blueprints
home = initHome(db)
search = initSearch(db)
posting = initPost(db)
dashboard = initDashBoard(db)
message =initChat(db, socket_io)


########## All the blue print is inside the views application #######
# Register blueprint
app.register_blueprint(home)
app.register_blueprint(search)
app.register_blueprint(posting)
app.register_blueprint(dashboard)
app.register_blueprint(profile)
app.register_blueprint(message)

socket_io.init_app(app)



if __name__ == "__main__":
    socket_io.run(app, debug=True)