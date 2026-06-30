from flask import Blueprint,render_template,request,redirect,session,abort
import config
from models.product import Product
from extensions import db

app=Blueprint("admin",__name__)


@app.before_request
def before_request_func():
    if session.get('admin_login',None) is None and request.endpoint != "admin.Login":
        abort(403)

@app.route('/admin/login',methods=["POST","GET"])
def Login():
    if request.method=="POST":
        username=request.form.get('username',None)
        password=request.form.get('password',None)
        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session['admin_login']=username
            return redirect("/admin/dashboard")
        else:
            return redirect("/admin/login")
    else:
        return render_template("admin/login.html")
    
@app.route('/admin/dashboard',methods=["GET"])
def dashbord():
    return render_template("admin/dashboard.html")


@app.route('/admin/dashboard/products',methods=["GET","POST"])
def product():
    if request.method == "GET":
        products = Product.query.all()
        return render_template("admin/products.html",products=products)
    else:
        name=request.form.get('name',None)
        price=request.form.get('price',None)
        description=request.form.get('description',None)
        active=request.form.get('active',None)

        p=Product(name=name,price=price,description=description)
        if active == None:
            p.active = 0
        else:
            p.active= 1
        
        db.session.add(p)
        db.session.commit()

        return "down"
