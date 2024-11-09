from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#first
class User_Login(db.Model):
    __tablename__ ="user_login"
    id = db.column(db.Integer,primary_key=True)
    email = db.column(db.String,unique = True,nullable =False)
    password = db.column(db.String,nullable = False)
    role = db.column(db.Integer)

class Customer(db.Model):
    __tablename__ ="customer"
    id = db.column(db.Integer,primary_key=True)
    full_name = db.column(db.String,nullable = False)
    address = db.column(db.String,nullable = False)
    pincode = db.column(db.Integer,nullable = False)


class professional(db.Model):
    __tablename__ ="professional"
    id = db.column(db.Integer,primary_key=True)
    full_name = db.column(db.String,nullable = False)
    experience = db.column(db.Integer,nullable = False)
    address = db.column(db.String,nullable = False)
    pincode = db.column(db.Integer,nullable = False)


#class service(db.model):
#    id = db.column(db.Integer,primary_key=True)
 #   name = db.column(db.string,nullable = False)

class service(db.Model):
    __tablename__ ="service"
    id = db.column(db.Integer,primary_key=True)
    name = db.column(db.String,nullable = False)
    description = db.column(db.String,nullable = False)
    base_price = db.column(db.Float,nullable = False)
    time_required = db.column(db.Integer,nullable = False)

class service_request(db.Model):
    __tablename__ ="service_request"
    id = db.column(db.Integer,primary_key=True)
    status  = db.column(db.String,nullable = False)
    date = db.column(db.DateTime,nullable = False)
    rating = db.column(db.Integer,default = 0)
    remark = db.column(db.string,nullable = False)