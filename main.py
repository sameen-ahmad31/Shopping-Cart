import sqlite3
from flask import Flask, session, render_template, redirect, url_for, request

app = Flask('app')
app.secret_key = "sameen"

@app.route('/')
def home_page():
  if 'name' in session: 
    return redirect('/userloggedin')
    
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cur = connection.cursor()
  cur.execute("select * from product")
  connection.commit()
  data = cur.fetchall()
  connection.commit()
  return render_template("home.html", title = 'Café de España', data = data)


@app.route('/coffeebeans' , methods=['GET', 'POST'])
def coffeebeans():
  if request.method == "GET":
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    cur.execute("select * from product where category_id is 10")
    connection.commit()
    coffbeans = cur.fetchall()
    connection.commit()
    return render_template("coffeebeans.html", coffbeans = coffbeans)
    
  if request.method == 'POST':
    return redirect('/')


@app.route('/groundcoffee', methods=['GET', 'POST'])
def groundcoffee():
  if request.method == "GET":
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    cur.execute("select * from product where category_id is 11")
    connection.commit()
    grndcafe = cur.fetchall()
    connection.commit()
    return render_template("groundcoffee.html", grndcafe = grndcafe)
    
  if request.method == 'POST':
    return redirect('/')


@app.route('/miscellaneous', methods=['GET', 'POST'])
def miscellaneous():
  if request.method == "GET":
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    cur.execute("select * from product where category_id is 12")
    connection.commit()
    misllc = cur.fetchall()
    connection.commit()
    return render_template("miscellaneous.html", misllc = misllc)
    
  if request.method == 'POST':
    return redirect('/')


@app.route('/userlogin', methods=['GET', 'POST'])
def login():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cur = connection.cursor()

  # If the username/password is correct, log them in and redirect them to the home page. Remember to set your session variables!
  if request.method == "GET":
    return render_template("login.html")

  if request.method == 'POST':
    uname = (request.form["username"])
    passwrd = (request.form["password"])
    cur.execute("SELECT username, password, fname, lname FROM user WHERE username = ? and password = ?", (uname, passwrd))
    data = cur.fetchone()
    connection.commit()
  
  if data != None :
    session['name'] = data['username']
    session['fname'] = data['fname']
    session['lname'] = data['lname']
    session['cart'] = list()
    return redirect('/userloggedin')
  else:
    return render_template("incorrect.html")


@app.route('/userloggedin')
def user():
  if 'name' in session: 
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    cur.execute("select * from product")
    data = cur.fetchall()
    connection.commit()
    return render_template("user.html", title = 'User Logged In', data = data)
  return redirect('/')


@app.route('/search', methods=['GET', 'POST'])
def search():
  if request.method == "GET":
    return render_template("search.html")
    
  if request.method == "POST":
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    srch = str((request.form["searchresult"]))
    cur.execute("SELECT * FROM product WHERE name LIKE ?", ('%' + srch + '%',))
    searchresults = cur.fetchall()
    return render_template("searchresult.html", searchresults = searchresults)


@app.route('/searchinOrders', methods=['GET', 'POST'])
def searchOrder():
  if request.method == "GET":
    return render_template("searchinord.html")
    
  if request.method == "POST":
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    srch = str((request.form["searchresult"]))
    cur.execute("SELECT * FROM orderItem WHERE product_name LIKE ?", ('%' + srch + '%',))
    searchresults = cur.fetchall()
    cur.execute("SELECT id, stock FROM product")
    productresults = cur.fetchall()
    return render_template("searchresultord.html", searchresults = searchresults, productresults = productresults)
  

@app.route('/cart', methods=['GET', 'POST'])
def cart():
  if request.method == "GET":
    return render_template("cart.html")
    
  if request.method == "POST":
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    prodid = int(request.form["id"])
    cur.execute("SELECT name, price, stock FROM product WHERE id = ?", (prodid,))
    productinfo = cur.fetchone()
    productname = productinfo['name']
    productprice = productinfo['price']
    stock = productinfo['stock']
    
    if (request.form["quant"]):
      quant = int(request.form["quant"])
    else:
      return render_template("cart.html")
    
    x = 1
    empt = False
    
    if(quant > stock):
      return render_template("cart.html")
    
    if len(session['cart']) == 0:
      #item = {"product id": prodid, "quantity": quant, "product name": productname, "price": productprice}
      cart = session['cart'] 
      cart.append([prodid, quant, productname, productprice])
      session['cart'] = cart
      empt = True

    if(empt == False):
      for i in session['cart']:
        if i[0] == prodid:
          q = i[1] + quant
          
          if(q > stock or stock == 0):
            #set the stock number to 0
            return render_template("cart.html")
          
          elif(q <= 0):
            cart = session['cart']
            cart.pop(cart.index(i))
            session['cart'] = cart
            
          else:
            cart = session['cart']
            cart[session['cart'].index(i)][1] = q
            session['cart'] = cart
          x += 1
          break
      
      if(x == 1):
       # items = {"product id": prodid, "quantity": quant, "product name": productname, "price": productprice}
        cart = session['cart']
        cart.append([prodid, quant, productname, productprice])
        session['cart'] = cart

    return render_template("cart.html")


@app.route('/prod/<idnum>')
def productname(idnum):
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cur = connection.cursor()
  connection.commit()
  cur.execute("SELECT id, name, price, stock, pic, description FROM product WHERE id = ?", (idnum,))
  proddata = cur.fetchone()
  return render_template("proddescrip.html", proddata = proddata)
  
  

@app.route('/clearcart')
def clearcart():
  session['cart'] = list()
  return render_template("cart.html")


@app.route('/sortorder', methods=['GET', 'POST'])
def sortOrder():
  if request.method == "GET":
    redirect('/orderhistory')
    
  if request.method == "POST":
    print("reaches here")
    id = (request.form["dates"])
    if(id == "desc"):
      return redirect('/sortorderdes')
    else:
      connection = sqlite3.connect("myDatabase.db")
      connection.row_factory = sqlite3.Row
      cur = connection.cursor()
      connection.commit()
      cur.execute("SELECT * FROM orderItem WHERE user_email = ? ORDER BY dateOfOrd ASC", (session['name'],))
      orderhist = cur.fetchall()
      return render_template("orderhistory.html", orderhist = orderhist)


@app.route('/sortorderdes')
def sortOrderDes():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cur = connection.cursor()
  connection.commit()
  cur.execute("SELECT * FROM orderItem WHERE user_email = ? ORDER BY dateOfOrd DESC", (session['name'],))
  orderhist = cur.fetchall()
  return render_template("orderhistory.html", orderhist = orderhist)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == "GET":
    return render_template("signup.html")
    
  if request.method == "POST":
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()
    unm = (request.form["username"])
    passwrd = (request.form["password"])
    fname = (request.form["fname"])
    lname = (request.form["lname"])
    
    cur.execute("SELECT username FROM user WHERE username = ?", (unm, ))
    connection.commit()
    data = cur.fetchone()
    if(data != None):
      return render_template("userexists.html")
      
    cur.execute("INSERT into user (username, password, fname, lname) VALUES (?, ?, ?, ?)", (unm, passwrd, fname, lname))
    connection.commit()
    
    cur.execute("SELECT username, password, fname, lname FROM user WHERE username = ? and password = ?", (unm, passwrd))
    data = cur.fetchone()
    connection.commit()
  
    if data != None :
      session['name'] = data['username']
      session['fname'] = data['fname']
      session['lname'] = data['lname']
      session['cart'] = list()
      return redirect('/userloggedin')


@app.route('/checkout')
def checkout():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cur = connection.cursor()
  for i in session['cart']:
    cur.execute("SELECT stock FROM product WHERE id = ?", (i[0],))
    num = cur.fetchone()
    stocknum = num['stock']
    newstocknum = stocknum - i[1]
    connection.commit()
    cur.execute("UPDATE product SET stock = ? WHERE id = ?", (newstocknum,i[0]))
    connection.commit()
    
    cur.execute("INSERT into orderItem (id, user_email, dateOfOrd, product_id, product_name, quantity) VALUES (?, ?, date('now'), ?, ?, ?)", (i[0], session['name'], i[0], i[2], i[1]))
    connection.commit()

    
  session['cart'] = list()
  return render_template("checkout.html")


@app.route('/orderhistory')
def orderhistory():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cur = connection.cursor()
  connection.commit()
  cur.execute("select * from orderItem where user_email = ?", (session['name'],))
  orderhist = cur.fetchall()
  return render_template("orderhistory.html", orderhist = orderhist)

  
@app.route('/logout')
def logout():
  session.pop('name', None)
  session.pop('fname', None)
  session.pop('lname', None)
  session.pop('cart', None)
  session.clear()
  return redirect('/')
  
app.run(host='0.0.0.0', port=8080)
