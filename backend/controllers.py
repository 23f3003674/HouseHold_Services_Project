from flask import Flask, render_template,request,url_for,redirect
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
            
            return redirect(url_for("admin_dashboard",name=uname))

        elif usr and usr.role ==1 and usr.status=="approve":
            return redirect(url_for("customer_dashboard",name=uname))
        
        elif usr and usr.role ==2 and usr.status=="approve":
            return redirect(url_for("professional_dashboard",name=uname))
        
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
        service_name = request.form.get("service")

        service =Service.query.filter_by(name=service_name).first()
        pservice_id =service.id

        new_usr1= Professional(full_name=full_name,address=address,pincode=pincode,experience=experience,service_id = pservice_id)
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
    return render_template("admin_dashboard.html",name=name,services=services)

@app.route("/customer/<name>")
def customer_dashboard(name):
    services = get_services()
    return render_template("customer_dashboard.html",name=name,services=services)

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

#def get_services_request():
 #   Service_requests = Service_request.query.all()
  #  return service_requests

#@app.route("/service_rating/<name>",methods=["POST","GET"])
#def add_service(name):
 #   if request.method =="POST":
  #      srating=request.form.get("rating")
  #      sremark=request.form.get("remark")
        
  #      new_service_request = Service_request(rating=srating,remark=sremark)
  #      db.session.add(new_service_request)
  #      db.session.commit()

   #     return redirect(url_for("customer_dashboard",name=name))

   # return render_template("service_rating.html",name=name)