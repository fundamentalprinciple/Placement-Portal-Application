from application.tasks import send_email
from flask import Flask
from application.config import Config
from flask_mail import Mail

app=Flask(__name__)

app.config.from_object(Config)
mail=Mail(app)

from flask import current_app
from application.tasks import send_email

with app.app_context():
    send_email('mysandbox@mailtrap.com','Test','Test body')
