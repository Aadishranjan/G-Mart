from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from db.database import db
from db.product import insert_product, products_collection, update_product

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
    
@app.route('/sales')
def sales():
    if session.get('username') == 'admin':
        return render_template('partials/sales.html')
    else:
        return render_template('partials/unauthorized.html')

@app.route('/stock')
def stock():
    products = list(products_collection.find())
    return render_template('partials/stock.html', products=products)

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
    
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_product(id):
    product = products_collection.find_one({'_id': ObjectId(id)})

    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        img = request.form['img']

        result = update_product(id, name, quantity, price, img, products_collection)

        if isinstance(result, dict) and result.get("error"):
            return render_template('edit.html', product=product, error=result["error"])

        return redirect(url_for('dashboard'))

    return render_template('edit.html', product=product)
  
@app.route('/delete/<id>', methods=['POST'])
def delete_product(id):
    products_collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)