from flask import Blueprint

app=Blueprint("admin",__name__)

@app.route('/admin')
def Admin():
    return "<h1> hello admin <h1/>"
