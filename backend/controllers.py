from flask import Flask, render_template,request
from .models import *
from flask import current_app as app

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def signin():
    if request.method =="POST":
        uname=request.form.get("user_name")
        pwd = request.form.get("password")
        usr= User_Login.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role ==0:
            return render_template("admin_dashboard.html")
    return render_template("login.html")

@app.route("/signup_customer")
def customer_signup():
    return render_template("signup_customer.html")

@app.route("/signup_professional")
def professional_signup():
    return render_template("signup_professional.html")