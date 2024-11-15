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

        elif usr and usr.role ==1 and usr.status=="approve":
            return render_template("customer_dashboard.html")
        
        elif usr and usr.role ==2 and usr.status=="approve":
            return render_template("professional_dashboard.html")
        
        else:
            return render_template("login.html",msg ="INVALID USER CREDENTIALS")

    return render_template("login.html",msg="")

@app.route("/signup_customer",methods=["GET","POST"])
def customer_signup():
    if request.method =="POST":
        uname=request.form.get("user_name")
        pwd = request.form.get("password")
        full_name=request.form.get("full_name")
        address=request.form.get("address")
        pincode= request.form.get("pincode")
        usr= User_Login.query.filter_by(email=uname).first()
        if usr:
            return render_template("login.html",msg="THIS MAIL IS ALREADY REGISTERED")

        new_usr1= Customer(full_name=full_name,address=address,pincode=pincode)
        db.session.add(new_usr1)
        db.session.commit()
        new_usr1_id = new_usr1.id
        new_usr = User_Login(email=uname,password=pwd,role=1,customer_id=new_usr1_id,status="approve")
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="REGISTERED SUCCESSFULLY!")

    return render_template("signup_customer.html")

@app.route("/signup_professional",methods=["GET","POST"])
def professional_signup():
    if request.method =="POST":
        uname=request.form.get("user_name")
        pwd = request.form.get("password")
        full_name=request.form.get("full_name")
        address=request.form.get("address")
        pincode= request.form.get("pincode")
        usr= User_Login.query.filter_by(email=uname).first()
        if usr:
            return render_template("login.html",msg="THIS MAIL IS ALREADY REGISTERED")

        experience= request.form.get("experience")
        service_name = request.form.get("service")
                  
        service = Service.query.filter_by(name = service_name).first()

        new_usr1= Professional(full_name=full_name,address=address,pincode=pincode,experience=experience,service_id=service.id)
        db.session.add(new_usr1)
        db.session.commit()
        new_usr1_id = new_usr1.id
        new_usr = User_Login(email=uname,password=pwd,role=2,professional_id=new_usr1_id,status="wait")
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html")

    return render_template("signup_professional.html")