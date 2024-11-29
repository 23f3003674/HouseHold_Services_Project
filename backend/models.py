from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
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
    status = db.Column(db.String)
    professional = db.relationship("Professional",cascade="all,delete",backref="user_login",lazy = True)
    customer = db.relationship("Customer",cascade="all,delete",backref="user_login",lazy = True)

class Customer(db.Model):
    __tablename__ ="customer"
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String)
    address = db.Column(db.String)
    pincode = db.Column(db.Integer)
    service_requests = db.relationship("Service_request",cascade="all,delete",backref="customer",lazy = True)


class Professional(db.Model):
    __tablename__ ="professional"
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String)
    experience = db.Column(db.Integer)
    address = db.Column(db.String)
    pincode = db.Column(db.Integer)
    service_requests = db.relationship("Service_request",cascade="all,delete",backref="professional",lazy = True)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"),nullable = False)


class Service(db.Model):
    __tablename__ ="service"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    base_price = db.Column(db.Float)
    time_required = db.Column(db.Integer)
    service_requests = db.relationship("Service_request",cascade="all,delete",backref="service",lazy = True)
    professionals = db.relationship("Professional",cascade="all,delete",backref="service",lazy = True) 
    service_pic_url = db.Column(db.String,nullable=True,default="None")


class Service_request(db.Model):
    __tablename__ ="service_request"
    id = db.Column(db.Integer,primary_key=True)
    status  = db.Column(db.String,default ="PENDING" )
    date = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    remark = db.Column(db.String)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"),nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"),nullable = False)
    professtional_id = db.Column(db.Integer, db.ForeignKey("professional.id"))
