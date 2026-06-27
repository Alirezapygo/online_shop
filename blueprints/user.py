from flask import Blueprint
import models.user

app=Blueprint("user",__name__)

@app.route('/user')
def User():
    return "<h1> hello user <h1/>"
