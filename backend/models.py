from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#first
class User_Login(db.Model):
    __tablename__ ="user_login"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,unique = True,nullable =False)
    password = db.Column(db.String,nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.id"))
    role = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String,nullable=False)

class Customer(db.Model):
    __tablename__ ="customer"
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String,nullable = False)
    address = db.Column(db.String,nullable = False)
    pincode = db.Column(db.Integer,nullable = False)
    #user_login_id = db.Column(db.Integer, db.ForeignKey("user_login.id"),nullable = False)
    service_requests = db.relationship("Service_request",cascade="all,delete",backref="customer",lazy = True)


class Professional(db.Model):
    __tablename__ ="professional"
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String,nullable = False)
    experience = db.Column(db.Integer,nullable = False)
    address = db.Column(db.String,nullable = False)
    pincode = db.Column(db.Integer,nullable = False)
    #user_login_id = db.Column(db.Integer, db.ForeignKey("user_login.id"),nullable = False)
    service_requests = db.relationship("Service_request",cascade="all,delete",backref="professional",lazy = True)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"),nullable = False)


#class service(db.model):
#    id = db.column(db.Integer,primary_key=True)
 #   name = db.column(db.string,nullable = False)

class Service(db.Model):
    __tablename__ ="service"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable = False)
    description = db.Column(db.String,nullable = False)
    base_price = db.Column(db.Float,nullable = False)
    time_required = db.Column(db.Integer,nullable = False)
    service_requests = db.relationship("Service_request",cascade="all,delete",backref="service",lazy = True)
    professionals = db.relationship("Professional",cascade="all,delete",backref="service",lazy = True) #


class Service_request(db.Model):
    __tablename__ ="service_request"
    id = db.Column(db.Integer,primary_key=True)
    status  = db.Column(db.String,nullable = False)
    date = db.Column(db.DateTime,nullable = False)
    rating = db.Column(db.Integer,default = 0)
    remark = db.Column(db.String)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"),nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"),nullable = False)
    professtional_id = db.Column(db.Integer, db.ForeignKey("professional.id"),nullable = False)
