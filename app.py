# Import Dependencies
from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
from functools import wraps
from flask_session import Session
import mysql.connector
import sqlCMD
import stripe
import random
import bcrypt
import json
import os

app = Flask(__name__)
stripe.api_key = 'sk_test_51K9EbHFyU4wB21ik92gItZpTKtZviOPc9uaZVBTdSGyHtgysMK2BPrRtNwvOu8eDcwPPMM4XfBgFA14KWGpbfatD00HFEuPoNf'
app.secret_key = 'super secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initiate Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='ecommerce'
)

# Initiate db.
mycursor = mydb.cursor(buffered=True)


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400



# Install Routes

@app.route('/')
def mainRoute():
  userName = session.get('name')
   
  return render_template('index.html', user=userName)

@app.route('/collection/<gender>')
def genderRoute(gender):
  userName = session.get('name')
  if gender == 'mens':
    mycursor.execute("SELECT * FROM products WHERE gender ='m'")
    myresult = mycursor.fetchall()
    return render_template('inventory.html', products=myresult, user=userName)

  if gender == 'womens':
    mycursor.execute("SELECT * FROM products WHERE gender ='w'")
    myresult = mycursor.fetchall()
    return render_template('inventory.html', products=myresult, user=userName)
  return redirect('/')




@app.route('/collection/item/<id>', methods = ['GET', 'POST'])
def fetchProductRoute(id):
  userName = session.get('name')
  if request.method == 'GET':
    mycursor.execute('SELECT * FROM products INNER JOIN inventory ON products.productID = inventory.productID  WHERE products.productID=%s' % (id))
    myresult = mycursor.fetchone()
    return render_template('show.html', product = myresult, user=userName)


  if request.method == 'POST':
    # 1. Check if a user is logged In.
    userID = session['userID']
    print('userID: ', userID)
    if userID:
      # If User, Find CartID.      
      # 1: CartItemID, 2: CartID, 3: productID, 4: size, 5: quantity
      mycursor.execute('SELECT * FROM carts WHERE carts.userID=%s' % (userID))
      results = mycursor.fetchone()
      cartID = results[0]
      print('CartID is: ',results)
    else:
      # Check if Cart.
      session["name"] = None
      session['userID'] = None
      cartID = session['cartID']
      print('CartID is: ', cartID)

      # If no cart, Create new one.
      if cartID == None:
        mycursor.execute("INSERT INTO carts (userID) VALUES (NULL)")
        print("Successfully Created Cart!")
        mydb.commit()
        cartID = mycursor.lastrowid
        session['cartID'] = cartID


    # Update items to cart.
    productID = request.form['productID']
    size = request.form['size']
    quantity = request.form['quantity']
    # Check if product exist for user & same size
    mycursor.execute('SELECT * FROM cartItem WHERE cartItem.cartID=%s AND cartItem.size="%s"' % (cartID,size))
    cart_item = mycursor.fetchone()
    print('my_cart', cart_item )
    if cart_item:
      quantity = int(quantity) + cart_item[4]
      mycursor.execute("UPDATE cartItem SET quantity = %s WHERE cartItemID = %s" % (quantity, cart_item[0]))
      print('Update Item in Cart')
      mydb.commit()
    else:

      mycursor.execute("INSERT INTO cartItem (cartID, productID, size, quantity) VALUES (%s, %s, '%s', %s)" % (cartID, productID, size, quantity))
      print("Successfully Added Item to Cart!")
      mydb.commit()
    return redirect('/cart')



@app.route('/cart')
def cart():
  userName = session['name']
  userID = session['userID']
  cartID = session['cartID']
  print('CartID: ', cartID)
  print('UserID: ', userID)
  print('Name: ', userName)
  mycursor.execute('SELECT * FROM products where products.gender = "w" LIMIT 3')
  w_suggestions = mycursor.fetchall()
  mycursor.execute('SELECT * FROM products where products.gender = "m" LIMIT 3')
  m_suggestions = mycursor.fetchall()
 

  # Get CardID
  if cartID:
    mycursor.execute('SELECT * FROM carts WHERE carts.cartID=%s' % (cartID))
    myresult = mycursor.fetchone()
    session['cartID'] = myresult[0]
    print(myresult)
    if myresult: 
      cartID = myresult[0]
      mycursor.execute('SELECT * FROM cartItem INNER JOIN products ON cartItem.productID = products.productID  WHERE cartItem.cartID=%s ' % (cartID))
      results = mycursor.fetchall()
      if results: 
        print(results)
        return render_template('cart/cart.html', cart=(results), w_suggestions=(None), m_suggestions=(None),user=userName)
      else:
        return render_template('cart/cart.html', cart=(None),w_suggestions=(w_suggestions),m_suggestions=(m_suggestions), user= userName)
    else:
        return render_template('cart/cart.html', cart=(None),w_suggestions=(w_suggestions),m_suggestions=(m_suggestions), user = userName)
  return render_template('cart/cart.html',cart=(None), w_suggestions=(w_suggestions),m_suggestions=(m_suggestions), user = userName)



@app.route('/auth/login', methods=['GET'])
def login():
    return render_template('auth/login.html')

@app.route('/auth/login', methods=['POST'])
def login_post():
  username = request.form['username']
  password = request.form['password']
  mycursor.execute("SELECT * FROM users WHERE username='" +(username) +"'")
  result=mycursor.fetchall()
  print('Length is: ')
  print(len(result))
  if(len(result) == 0):
    flash('Username or Password is Incorrect')
    return redirect('/auth/login')
  user = result[0]
  sql_password = user[3].encode('utf-8')
  if bcrypt.checkpw(password.encode('utf8'), sql_password):
    print('We Have a Match!')
    session["name"] = request.form.get("username")
    session['userID'] = result[0][0]

    mycursor.execute("SELECT * FROM carts where userID = %s" % (result[0][0]))
    myresult = mycursor.fetchone()  
    session['cartID'] = myresult[0]
    return redirect('/')
  else:
    flash('Username or Password is incorrect')
    return redirect('/auth/login')




@app.route('/auth/signup',  methods=['GET'])
def signup():
    return  render_template('auth/register.html')


@app.route('/auth/signup', methods=['POST'])
def signup_post():
    mycursor = mydb.cursor(buffered=True) 
    # code to validate and add user to database goes here
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    cartID = session['cartID']
    mycursor.execute("SELECT * FROM users WHERE username='" +(username) +"'")
    rows=mycursor.fetchall()
    if(len(rows) > 0):
      flash('Username or Email address already exists')
      return redirect('/auth/signup')
    else:
      mycursor.execute("SELECT * FROM users WHERE email='" +(email) +"'")
      rows=mycursor.fetchall()
      if(len(rows) > 0):
        flash('Username or Email address already exists')
        return redirect('/auth/signup')
      else:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
        val = (email, username, hashed)
        mycursor.execute(sql, val)
        # Create a Cart 
        mycursor.execute("SELECT * FROM users WHERE username='" +(username) +"'")
        item=mycursor.fetchall()
        userId = item[0][0]

        # Check if cart already exist.
        if cartID:
          mycursor = mydb.cursor()
          sql = "UPDATE carts SET userID = '%s' WHERE cartID = '%s'" % (userId,cartID)
          mycursor.execute(sql)
          mydb.commit()
          print("cartID: ", cartID)
        else:
          # Create Cart if no Cart.
          mycursor.execute("INSERT INTO carts (userID) VALUES (%s)" % (userId))
          print("Successfully Created Cart!")
          mydb.commit()
          cartID = mycursor.lastrowid
          print("cartID: ", cartID)
          session["name"] = request.form.get("username")
          session['userID'] = userId
          session['cartID'] = cartID


        return redirect('/cart')




@app.route("/auth/logout")
def logout():
    session["name"] = None
    session['userID'] = None
    session['cartID'] = None
    return redirect("/")


stripe.api_key = 'sk_test_51K9EbHFyU4wB21ik92gItZpTKtZviOPc9uaZVBTdSGyHtgysMK2BPrRtNwvOu8eDcwPPMM4XfBgFA14KWGpbfatD00HFEuPoNf'


@app.route('/create-checkout-session', methods=['GET'])
def get_checkout_session():
  return render_template('checkout.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1K9FHDFyU4wB21ikOa0PT9nn',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:5000/success',
            cancel_url='http://localhost:5000/cancel',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@app.route('/success', methods=['GET'])
def render_success():
  cartID = session['cartID']
  userID = session['userID']
  if cartID:
    sql = "DELETE FROM cartItem WHERE cartID = %s" % (cartID)
    mycursor.execute(sql)
    mydb.commit()
  print("SUCCEESSSSS!")
  return redirect('/cart')

@app.route('/cancel', methods=['GET'])
def render_cancel():
    return render_template('cart/cancel.html')


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='eur',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.before_first_request
def before_first_request():
    session["name"] = None
    session['userID'] = None
    session['cartID'] = None


if __name__ == '__main__':
  app.run(debug=True)
