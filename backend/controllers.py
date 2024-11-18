from flask import Flask, render_template,request,url_for,redirect
from .models import *
from flask import current_app as app
from datetime import date

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
            
            return redirect(url_for("admin_dashboard",name=uname))

        elif usr and usr.role ==1 and usr.status=="approve":
            c_id = usr.customer_id
            return redirect(url_for("customer_dashboard",id = c_id))
        
        elif usr and usr.role ==2 and usr.status=="approve":
            p_id = usr.professional_id
            return redirect(url_for("professional_dashboard",name=uname,id =p_id))
        
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
    services = get_services()
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
        service_name = request.form.get("service_name")

        service =Service.query.filter_by(name=service_name).first()
        pservice_id = service.id
        new_usr1= Professional(full_name=full_name,address=address,pincode=pincode,experience=experience,service_id=pservice_id)
        db.session.add(new_usr1)
        db.session.commit()
        new_usr1_id = new_usr1.id
        new_usr = User_Login(email=uname,password=pwd,role=2,professional_id=new_usr1_id,status="wait")
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html")

    return render_template("signup_professional.html",services=services)


# common route for admin
@app.route("/admin/<name>")
def admin_dashboard(name):
    services = get_services()
    professionals = get_professionals()
    user_logins = get_user_login()
    return render_template("admin_dashboard.html",name=name,services=services,professionals = professionals,user_logins=user_logins)


@app.route("/customer/<id>")
def customer_dashboard(id):
    #user_logins = get_user_login()
    # u = User_Login.query.filter_by(email=name).first()
    # u_id = u.customer_id
    customer = get_customer(id)
    services = get_services()
    return render_template("customer_dashboard.html",services=services,customer=customer,id=id)

@app.route("/professional/<name>")
def professional_dashboard(name):
    return render_template("professional_dashboard.html",name=name)



@app.route("/service/<name>",methods=["POST","GET"])
def add_service(name):
    if request.method =="POST":
        sname=request.form.get("name")
        sdescription=request.form.get("description")
        sbase_price=request.form.get("base_price")
        stime_required=request.form.get("time_required")
        new_service = Service(name=sname,description=sdescription,base_price=sbase_price,time_required=stime_required)
        db.session.add(new_service)
        db.session.commit()

        return redirect(url_for("admin_dashboard",name=name))

    return render_template("add_service.html",name=name)

def get_services():
    services = Service.query.all()
    return services

def get_professionals():
    professionals = Professional.query.all()
    return professionals

def get_customer(id):
    customer = Customer.query.filter_by(id=id).first()
    return customer

def get_user_login():
    user_logins = User_Login.query.all()
    return user_logins

@app.route("/update_professional/<name>",methods=["GET","POST"])
def approve_professional(name):
    if request.method == "POST":
    #user_logins = get_user_login()
        request_id = request.form.get("id")
        action = request.form.get("action")
        u = User_Login.query.filter_by(professional_id=request_id).first()
        if action =="approve":
            u.status = "approve"
            db.session.commit()
        elif action =="reject":
            u.status = "reject"
            db.session.commit()


        return redirect(url_for("admin_dashboard",name=name))
    

@app.route("/service_request/<id>", methods=["GET","POST"])
def add_service_request(id):
    if request.method=="POST":
        c_id = request.form.get("id")
        s_id = request.form.get("s_id")

        new_service_request = Service_request(customer_id=c_id,service_id=s_id)
        db.session.add(new_service_request)
        db.session.commit()
        
        return redirect(url_for("customer_dashboard",id =id))

@app.route("/search_ad/<name>",methods =["GET","POST"])
def search_ad(name):
    if request.method=="POST":
        professionals = get_professionals()
        user_logins = get_user_login()
        services = get_services()
        search_txt = request.form.get("search_txt")
        by_customers = search_by_customers(search_txt)
        by_professionals = search_by_professionals(search_txt)
        by_services = search_by_services(search_txt)
        if by_services:
            return render_template("admin_dashboard.html",name =name,services=by_services,professionals=professionals,user_logins=user_logins)
        elif by_professionals:
            return render_template("admin_dashboard.html",name =name,services=services,professionals1=by_professionals,professionals=professionals,user_logins=user_logins)
        elif by_customers:
            return render_template("admin_dashboard.html",name =name,services=services,customers1=by_customers,professionals=professionals,user_logins=user_logins)

    return redirect(url_for("admin_dashboard",name=name))

@app.route("/search_c/<id>",methods =["GET","POST"])
def search_c(id):
    if request.method=="POST":
        search_txt = request.form.get("search_txt")
        by_services = search_by_services(search_txt)
        if by_services:
            return render_template("customer_dashboard.html",id =id,services=by_services)

    return redirect(url_for("customer_dashboard",id=id))


# search functions

def search_by_customers(search_txt):
    customers = Customer.query.filter(Customer.full_name.ilike(f"%{search_txt}")).all()
    return customers

def search_by_professionals(search_txt):
    professionals = Professional.query.filter(Professional.full_name.ilike(f"%{search_txt}")).all()
    return professionals

def search_by_services(search_txt):
    services= Service.query.filter(Service.name.ilike(f"%{search_txt}")).all()
    return services
