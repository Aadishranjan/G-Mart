from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from db.database import db

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

    
@app.route("/sell")
def sell_page():
    return "<h2>Sell Page</h2>"

@app.route("/stock")
def stock_page():
    return "<h2>Stock Page</h2>"

@app.route("/sales")
def sales_report():
    if session.get("username") != "admin":
        return "Access denied", 403
    return "<h2>Sales Report</h2>"    

if __name__ == "__main__":
    app.run(debug=True)