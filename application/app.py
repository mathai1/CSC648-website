#Using blue print to structure the file
#Blueprint is the collection of views , static file and template
#In this application, the structure is divided  by its function
#The blueprint in views folder collections of views
#The same static files will be used for the views in most of the blueprints
# Most of the templates will extend a master template

from flask import Flask
from views.search import search
from views.home import home
from views.posting import posting
from views.dashboard import dashboard
from views.profile import profile

# Register blueprint into app
# All the blue print is inside the views application
app = Flask(__name__)
app.secret_key="SFSU"
app.register_blueprint(home)
app.register_blueprint(search)
app.register_blueprint(posting)
app.register_blueprint(dashboard)
app.register_blueprint(profile)




if __name__ == "__main__":
    app.run()