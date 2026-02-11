from flask import Flask
from config import Config

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.app_context().push()
    return app

app = create_app()

from routes.controllers import *

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)




