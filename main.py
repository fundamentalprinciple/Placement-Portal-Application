import os

from flask import Flask
from application.config import Config

from application.database import db

from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from application.models import User, Role


app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    
    db.init_app(app)
    
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    
    with app.app_context():
        db.create_all()

    with app.app_context():
        roles = ['admin', 'company', 'student']
        for name in roles:
            if not Role.query.filter_by(name=name).first():
                db.session.add(Role(name=name))
                db.session.commit()

        admin_user = User.query.filter_by(email='admin@admin.com').first()
        if not admin_user:
            admin_user = User(email='admin@admin.com', password=hash_password(os.getenv('Admin')), active=True, fs_uniquifier='')
            db.session.add(admin_user)
            db.session.commit()


    app.app_context().push()
    return app

app = create_app()

from application.controllers import *

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)




