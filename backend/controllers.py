from flask import Flask, render_template,request,url_for,redirect
from .models import *
from flask import current_app as app
from datetime import date
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt

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
            return redirect(url_for("professional_dashboard",id =p_id))
        
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

        service = Service.query.filter_by(name =service_name).first()

        pservice_id = service.id
        new_usr1= Professional(full_name=full_name,address=address,pincode=pincode,experience=experience,service_id=pservice_id)
        db.session.add(new_usr1)
        db.session.commit()
        new_usr1_id = new_usr1.id
        new_usr = User_Login(email=uname,password=pwd,role=2,professional_id=new_usr1_id,status="wait")
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="REGISTERED SUCCESSFULLY!, WAIT FOR ADMIN APPROVAL!!")

    return render_template("signup_professional.html",services=services)


# common route for admin
@app.route("/admin/<name>")
def admin_dashboard(name):
    services = get_services()
    professionals = get_professionals()
    user_logins = get_user_login()
    custumers = Customer.query.all()
    service_requests = Service_request.query.all()
    return render_template("admin_dashboard.html",name=name,services=services,professionals = professionals,user_logins=user_logins,customers = custumers,service_requests=service_requests)


@app.route("/customer/<id>")
def customer_dashboard(id):
    #user_logins = get_user_login()
    # u = User_Login.query.filter_by(email=name).first()
    # u_id = u.customer_id
    customer = get_customer(id)
    services = get_services()
    services1 = get_services()
    service_requests = Service_request().query.filter_by(customer_id=id).all()
    return render_template("customer_dashboard.html",services=services,customer=customer,id=id,service_requests=service_requests,services1=services1)

@app.route("/professional/<id>")
def professional_dashboard(id):
    professional = Professional.query.filter_by(id=id).first()
    service_id = professional.service_id
    service = Service.query.filter_by(id=service_id).first()
    service_request = Service_request.query.filter_by(service_id=service_id).all()
    customers = Customer.query.all()
    return render_template("professional_dashboard.html",id=id,professional=professional,service =service,service_request=service_request,customers=customers)



@app.route("/service/<name>",methods=["POST","GET"])
def add_service(name):
    if request.method =="POST":
        sname=request.form.get("name")
        sdescription=request.form.get("description")
        sbase_price=request.form.get("base_price")
        stime_required=request.form.get("time_required")
        # file = request.files["file_upload"]
        # if file.filename:
        #     file_name =secure_filename(file.filename)
        #     url = './uploaded_files'+file_name
        #     file.save(url)

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
    services1 = get_services()
    services = get_services()
    service_requests = Service_request().query.filter_by(customer_id=id).all()
    if request.method=="POST":
        c_id = request.form.get("id")
        s_id = request.form.get("s_id")
        dt_time_now = datetime.today().strftime('%Y-%m-%dT%H:%M')
        dt_time_now = datetime.strptime(dt_time_now,"%Y-%m-%dT%H:%M")


        new_service_request = Service_request(customer_id=c_id,service_id=s_id,date=dt_time_now)
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
        customers = Customer.query.all()
        service_requests = Service_request.query.all()
        if by_services:
            return render_template("admin_dashboard.html",name =name,services=by_services,professionals=professionals,user_logins=user_logins,customers=customers,service_requests=service_requests)
        elif by_professionals:
            return render_template("admin_dashboard.html",name =name,services=services,professionals1=by_professionals,professionals=professionals,user_logins=user_logins,customers=customers,service_requests=service_requests)
        elif by_customers:
            return render_template("admin_dashboard.html",name =name,services=services,customers1=by_customers,professionals=professionals,user_logins=user_logins,customers=customers,service_requests=service_requests)

    return redirect(url_for("admin_dashboard",name=name))

@app.route("/search_c/<id>",methods =["GET","POST"])
def search_c(id):
    # customer = get_customer(id)
    services1 = get_services()
    service_requests = Service_request().query.filter_by(customer_id=id).all()
    customer=Customer.query.filter_by(id=id).first()
    if request.method=="POST":
        search_txt = request.form.get("search_txt")
        by_services = search_by_services(search_txt)
        if by_services:
            return render_template("customer_dashboard.html",id =id,services=by_services,customer=customer,service_requests=service_requests,services1=services1)

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

@app.route("/edit_service/<id>/<name>" ,methods = ["GET","POST"])
def edit_service(id,name):
    service = get_service(id)
    if request.method =="POST":

        sname = request.form.get("name")
        description = request.form.get("description")
        base_price = request.form.get("base_price")
        time_required = request.form.get("time_required")
        service.name = sname
        service.description = description
        service.base_price = base_price
        service.time_required = time_required
        db.session.commit()
        return redirect(url_for("admin_dashboard",name =name))
    return render_template("edit_service.html",service=service,name=name)


def get_service(id):
    service = Service.query.filter_by(id=id).first()
    return service

@app.route("/delete_service/<id>/<name>" ,methods = ["GET","POST"])
def delete_service(id,name):
    pro = Professional.query.filter_by(service_id=id).all()
    for p in pro:
        pro_id = p.id
        Ul = User_Login.query.filter_by(professional_id=pro_id).first()
        Ul.status ="reject"

    service = get_service(id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name =name))

@app.route("/customer_profile/<id>" ,methods = ["GET","POST"])
def customer_profile(id):
    customer = get_customer(id)
    if request.method =="POST":

        cname = request.form.get("full_name")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        customer.full_name = cname
        customer.address = address
        customer.pincode = pincode
        db.session.commit()
        return redirect(url_for("customer_dashboard",id=id))
    return render_template("customer_profile.html",customer =customer,id=id)

@app.route("/professional_profile/<id>",methods = ["GET","POST"])
def professional_profile(id):
    professional = Professional.query.filter_by(id=id).first()
    if request.method =="POST":

        pname = request.form.get("full_name")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        experience = request.form.get("experience")
        professional.full_name = pname
        professional.address = address
        professional.pincode = pincode
        professional.experience = experience
        db.session.commit()
        return redirect(url_for("professional_dashboard",id=id))
    return render_template("professional_profile.html",professional =professional,id=id)


@app.route("/accept_service/<id>",methods=["GET","POST"])
def accept_service(id):
    if request.method == "POST":
    #user_logins = get_user_login()
        p_id = request.form.get("id")
        service_request_id = request.form.get("service_request_id")
        service_request = Service_request.query.filter_by(id=service_request_id).first()
        service_request.professtional_id = p_id
        service_request.status = "ACCEPTED"
        db.session.commit()
        return redirect(url_for("professional_dashboard",id=id))
    

@app.route("/block_professional/<name>", methods =["POST","GET"])
def block_professional(name):
    if request.method == "POST":
        user_id = request.form.get("id")
        p = User_Login.query.filter_by(professional_id=user_id).first()
        service_requests = Service_request.query.filter_by(professtional_id=user_id).all()
        if p:
            p.status = "reject"
            for sr in service_requests:
                if sr.status != "COMPLETED":
                    sr.professtional_id = None
                    sr.status = "PENDING"

            db.session.commit()
            return redirect(url_for("admin_dashboard",name =name))
        

@app.route("/block_customer/<name>", methods =["POST","GET"])
def block_customer(name):
    if request.method == "POST":
        user_id = request.form.get("id")
        c = User_Login.query.filter_by(customer_id =user_id).first()
        service_requests = Service_request.query.filter_by(customer_id=user_id).all()
        if c :
            c.status = "reject"
            for sr in service_requests:
                db.session.delete(sr)

            db.session.commit()
            return redirect(url_for("admin_dashboard",name =name))


@app.route("/close_service_request/<id>/<service_request_id>",methods = ["GET","POST"])
def close_service_request(id,service_request_id):
    service_request = Service_request.query.filter_by(id=service_request_id).first()
    professtional_id = service_request.professtional_id
    professional = Professional.query.filter_by(id=professtional_id).first()
    service_id = service_request.service_id
    service =Service.query.filter_by(id=service_id).first()
    customer = get_customer(id)

    if request.method == "POST":
        rating = request.form.get("service_rating")
        remark = request.form.get("service_remark")
        service_request.rating = rating
        service_request.remark = remark
        service_request.status="COMPLETED"
        db.session.commit()
        return redirect(url_for("customer_dashboard",id=id))
    return render_template("close_service_request.html",professional=professional,id=id,service_request=service_request,service=service,customer=customer,service_request_id=service_request_id)

@app.route("/edit_service_request/<id>/<service_request_id>",methods = ["GET","POST"])
def edit_service_request(id,service_request_id):
    service_request = Service_request.query.filter_by(id=service_request_id).first()
    service_id = service_request.service_id
    service =Service.query.filter_by(id=service_id).first()
    customer = get_customer(id)
    #dt_time_now = datetime.today().strftime('%Y-%m-%d')
    

    if request.method == "POST":
        service_request_date = request.form.get("service_request_date")
        service_request_udate = datetime.strptime(service_request_date,"%Y-%m-%dT%H:%M")
        service_request.date = service_request_udate
        db.session.commit()
        return redirect(url_for("customer_dashboard",id=id))
    return render_template("edit_service_request.html",id=id,service_request=service_request,service=service,customer=customer,service_request_id=service_request_id)

def get_services_summary():
    services = Service.query.all()
    summary={}
    for s in services:
        summary[s.name]=s.base_price
    x_name = list(summary.keys())
    y_base_price=list(summary.values())
    plt.bar(x_name,y_base_price,color="blue",width=0.4)
    plt.title("SERVICE/PRICE")
    plt.xlabel("SERVICES")
    plt.ylabel("PRICE")
    return plt

def get_services_request_summary():
    Service_requests = Service_request.query.all()
    summary={
        "PENDING" : 0,
        "ACCEPTED" : 0,
        "COMPLETED" : 0
    }
  
    for s in Service_requests:
        if s.status in summary:
            summary[s.status] += 1
    x_name = list(summary.keys())
    y_count=list(summary.values())
    plt.bar(x_name,y_count,color="blue",width=0.4)
    plt.title("SERVICE_REQUEST_STATUS")
    plt.xlabel("STATUS")
    plt.ylabel("NUMBER")
    return plt

# def get_ad_professional_summary():
#     Service_requests = Service_request.query.all()
#     professional_rating={}
#     for s in Service_requests:
#         if s.professtional_id not in professional_rating:
#             professional_rating[s.professtional_id] = {'total_rating' : 0 , 'count' :0}
#         professional_rating[s.professtional_id]['total_rating'] += s.rating
#         professional_rating[s.professtional_id]['count'] += 1

#     average = {}
#     for professtional_id , data in professional_rating.items():
#         average[professtional_id] = data['total_rating']/data['count']

#     x_name = list(average.keys())
#     y_count=list(average.values())
#     plt.bar(x_name,y_count,color="blue",width=0.4)
#     plt.title("PROFESSIONAL_RATING")
#     plt.xlabel("PROFESSIONAL_ID")
#     plt.ylabel("RATING")
#     return plt

# summaries

@app.route("/admin_summary")
def admin_summary():
    plot=get_services_summary()
    plot.savefig("./static/styles/images/service_summary.jpeg")
    plot.clf()
    plot1=get_services_request_summary()
    plot1.savefig("./static/styles/images/service_request_summary.jpeg")
    plot1.clf()
    # plot2 = get_ad_professional_summary()
    # plot2.savefig("./static/styles/images/professional_rating_summary.jpeg")
    # plot2.clf()
    return render_template("admin_summary.html")


def get_customer_summary(id):
    Service_requests = Service_request.query.filter_by(customer_id = id)
    summary={
        "PENDING" : 0,
        "ACCEPTED" : 0,
        "COMPLETED" : 0
    }
  
    for s in Service_requests:
        if s.status in summary:
            summary[s.status] += 1
    x_name = list(summary.keys())
    y_count=list(summary.values())
    plt.bar(x_name,y_count,color="blue",width=0.4)
    plt.title("CUSTOMER SERVICE REQUEST")
    plt.xlabel("STATUS")
    plt.ylabel("NUMBER")
    return plt

@app.route("/customer_summary/<id>")
def customer_summary(id):
    customer= Customer.query.filter_by(id=id).first()
    plot=get_customer_summary(id)
    image_filename = f'customer{id}_summary.jpeg'
    image_path = f'./static/styles/images/{image_filename}'
    plot.savefig(image_path)
    plot.clf()
    return render_template("customer_summary.html",image_filename = image_filename,customer=customer)

def get_professional_summary(id):
    Service_requests = Service_request.query.filter_by(professtional_id = id)
    summary={
        "ACCEPTED" : 0,
        "COMPLETED" : 0
    }
  
    for s in Service_requests:
        if s.status in summary:
            summary[s.status] += 1
    x_name = list(summary.keys())
    y_count=list(summary.values())
    plt.bar(x_name,y_count,color="blue",width=0.4)
    plt.title("PROFESSIONAL SERVICE REQUEST")
    plt.xlabel("STATUS")
    plt.ylabel("NUMBER")
    return plt

@app.route("/professional_summary/<id>")
def professional_summary(id):
    professional= Professional.query.filter_by(id=id).first()
    plot=get_professional_summary(id)
    image_filename = f'professional{id}_summary.jpeg'
    image_path = f'./static/styles/images/{image_filename}'
    plot.savefig(image_path)
    plot.clf()
    return render_template("professional_summary.html",image_filename = image_filename,professional=professional)
