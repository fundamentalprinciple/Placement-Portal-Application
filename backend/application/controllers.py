from flask import Flask, render_template
from flask import current_app as app

from flask_security import auth_required

@app.route("/")
def root():
    return "root" 

@app.route("/protected")
@auth_required("token")
def protected():
    return "protected"
