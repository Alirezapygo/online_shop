from flask import Flask
from flask_wtf.csrf import CSRFProtect
from blueprints.general import app as general 
from blueprints.admin import app as admin 
from blueprints.user import app as user 
import config 
import extensions

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"]= config.SECRET_KEY
extensions.db.init_app(app)

csrf = CSRFProtect(app)

with app.app_context():
    extensions.db.create_all()
app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)



if __name__ == '__main__':
    app.run(debug=True)