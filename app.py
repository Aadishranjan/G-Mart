from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from db.database import db
from db.product import insert_product, products_collection

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flashing

user_collection = db["user"]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = user_collection.find_one({"username": username, "password": password})
        if user:
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session['username'])
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login')) 
    
@app.route('/sell')
def sell():
    return render_template('partials/sell.html')
    
@app.route('/stock')
def stock():
    products = list(products_collection.find())
    return render_template('partials/stock.html', products=products)

@app.route('/sales')
def sales():
    if session.get('username') == 'admin':
        return render_template('partials/sales.html')
    else:
        return render_template('partials/unauthorized.html')

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['product_name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        img = request.form['img_link']

        success = insert_product(name, quantity, price, img)
        if success:
            return redirect(url_for('dashboard'))  # or another success page
        else:
            return render_template('add.html', message="Product already exists!")

    return render_template('add.html')

if __name__ == "__main__":
    app.run(debug=True)