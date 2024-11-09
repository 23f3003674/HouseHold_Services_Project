from flask import Flask


app =None


def setup_app():
    app =Flask(__name__)
    app.debug=True
    #pending sqlite connection
    app.app_context().push() #direct access to other modules
    print("app is starting....")
    
setup_app()

from backend.controllers import *

if __name__ =="__main__":
    app.run()