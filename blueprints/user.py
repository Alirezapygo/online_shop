from flask import Blueprint,render_template,request,redirect,url_for,flash
from models.user import User
from extensions import db
from passlib.hash import sha256_crypt
from flask_login import login_user

app=Blueprint("user",__name__)

@app.route('/user/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        register=request.form.get('register',None)
        username=request.form.get('username',None)
        password=request.form.get('password',None)
        phone=request.form.get('phone',None)
        address=request.form.get('address',None)


        if register!=None:
            user = User.query.filter(User.username == username).first()
            if user != None:
                flash('نام کاربری دیگر انتخاب کنید')
                return redirect(url_for('user.login'))
            
            user = User(username = username ,password = sha256_crypt.encrypt(password), phone = phone , address=address)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/user/dashboard')
        

        else:
            user = User.query.filter(User.username == username).first()
            if user == None:
                flash('نام کاربری یا پسورد اشتباه است')
                return redirect(url_for('user.login'))

            if  sha256_crypt.verify(password , user.password):
                login_user(user)
                return redirect('/user/dashboard')
            else:
                flash('نام کاربری یا پسورد اشتباه است')
                return redirect(url_for('user.login'))
            
        return "down"