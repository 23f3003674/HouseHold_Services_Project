from flask import Flask
from backend.models import db

app =None


def setup_app():
    app =Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///A-Z_HOUSEHOLD_SERVICE.sqlite3" # having db file
    db.init_app(app) #flask app connected to db(SQL alchemy)
    app.app_context().push() #direct access to other modules
    app.debug=True
    print("app is starting....")
    
setup_app()

from backend.controllers import *

if __name__ =="__main__":
    app.run()