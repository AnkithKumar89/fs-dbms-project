from app import db,login,admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
    
class Students(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    usn=db.Column(db.String,index=True)
    name=db.Column(db.String,index=True)
    yoa = db.Column(db.Integer,index=True)
    specialization = db.Column(db.String(5),index=True)
    semester = db.Column(db.Integer,index=True)
    age = db.Column(db.Integer, index=True)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    section=db.Column(db.String(1))

    def to_dict(self):
        return {
            'id': self.id,
            'usn':self.usn,
            'name': self.name,
            'yoa':self.yoa,
            'specialization':self.specialization,
            'semester':self.semester,
            'age': self.age,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'section':self.section,
        }


class Faculty(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

db.create_all()

@login.user_loader
def load_user(id):
    return Faculty.query.get(int(id))

admin.add_view(ModelView(Students,db.session))
admin.add_view(ModelView(Faculty,db.session))