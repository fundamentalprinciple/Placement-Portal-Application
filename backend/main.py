import os
from flask import Flask

from application.config import Config
from application.database import db
from application.models import User

from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api

app,api = None,None

def create_app():
    app = Flask(__name__)
    api = Api(app)
    bcrypt = Bcrypt(app)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    with app.app_context():
        admin_user = User.query.filter_by(email='admin@admin.com').first()
        if not admin_user:
            admin_user = User(username='admin',email='admin@admin.com', password=bcrypt.generate_password_hash(os.getenv('Admin')), role='admin')
            db.session.add(admin_user)
            db.session.commit()


    app.app_context().push()
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173/*"}})
    return app,api

app,api = create_app()


from application.controllers import *
from application.api import UserRegisteration, UserLogin, Secure

api.add_resource(UserRegisteration, '/register', endpoint="register")
api.add_resource(UserLogin, '/login', endpoint="login")
api.add_resource(Secure, '/secure', endpoint="secure")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)




