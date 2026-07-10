from flask import Blueprint,render_template,request,redirect,url_for,flash
from models.user import User
from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
from models.payment import Payment
from extensions import db
from passlib.hash import sha256_crypt
from flask_login import login_user,login_required,current_user
import config
import requests

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
            return redirect(url_for('user.dashboard'))
        

        else:
            user = User.query.filter(User.username == username).first()
            if user == None:
                flash('نام کاربری یا پسورد اشتباه است')
                return redirect(url_for('user.login'))

            if  sha256_crypt.verify(password , user.password):
                login_user(user)
                return redirect(url_for('user.dashboard'))
            else:
                flash('نام کاربری یا پسورد اشتباه است')
                return redirect(url_for('user.login'))
            
        return "down"
    

@app.route('/add-to-cart',methods=['GET'])
@login_required
def add_to_cart():
    id = request.args.get('id')

    product = Product.query.filter(Product.id == id ).first_or_404()

    cart=current_user.carts.filter(Cart.status == 'pending').first()

    if cart == None:
        cart=Cart()
        current_user.carts.append(cart)
        db.session.add(cart)

    cart_item=cart.cart_items.filter(CartItem.product == product).first()
    if cart_item == None:
        item = CartItem(quantity = 1)
        item.price = product.price
        item.cart = cart
        item.product = product
        db.session.add(item)
    else:
        cart_item.quantity += 1

      
    db.session.commit()

    return redirect(url_for('user.cart'))

@app.route('/cart',methods=['GET'])
@login_required
def cart():
    cart = current_user.carts.filter(Cart.status=='pending').first()
    return render_template('user/cart.html', cart=cart)  


@app.route('/payment',methods=['GET'])
@login_required
def payment():
    cart = current_user.carts.filter(Cart.status=="pending").first()
    r=requests.post('https://gateway.zibal.ir/v1/request',
                    json={
                        'merchant':'zibal',
                        'amount':cart.total_price(),
                        'description':'درگاه پرداخت',
                        'callbackUrl':'http://localhost:5000/verify'
                        })
    track_id=r.json()['trackId']
    payment_url = f'https://gateway.zibal.ir/start/{track_id}'
    pay = Payment(price = cart.total_price(),track_id=track_id)
    pay.cart = cart
    db.session.add(pay)
    db.session.commit()
    return redirect(payment_url)
    
@app.route('/verify',methods=['GET'])
@login_required
def verify():
    trackId = request.args.get('trackId')
    pay = Payment.query.filter(Payment.track_id==trackId).first_or_404()
    r=requests.post('https://gateway.zibal.ir/v1/verify',
                    json={
                        'merchant':'zibal',
                        'trackId':trackId
                        })
    response_data = r.json()
    if response_data.get('result') == 100:
        transaction_id = response_data.get('trackId')
        card_pan = response_data.get('cardNumber')
        refid = response_data.get('refNumber')
        pay.card_pan=card_pan
        pay.transaction_id=transaction_id
        pay.refid=refid
        pay.status='success'
        pay.cart.status= 'paid'
        flash('پرداخت موفق آمیز بود')
    else:
         pay.status='failde'
         flash('پرداخت نا موفق بود')

    db.session.commit()

    return redirect(url_for('user.dashboard'))




@app.route('/user/dashboard',methods=['GET'])
@login_required
def dashboard():
    return "dashboard page"



@app.route('/remove-from-cart',methods=['GET'])
@login_required
def remove_from_cart():
    id = request.args.get('id')

    cart_item = CartItem.query.filter(CartItem.id == id ).first_or_404()
    if cart_item.quantity > 1:
        cart_item.quantity -=1
    else:
        db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('user.cart'))