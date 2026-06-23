from flask import Blueprint

app=Blueprint("general",__name__)

@app.route('/')
def Home():
    return "<h1> hello world <h1/>"
