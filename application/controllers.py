from flask import Flask, render_template
from flask import current_app as app

@app.route("/")
def root():
    return render_template("index.html")
