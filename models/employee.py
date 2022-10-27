from init import db, ma

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    action = db.Column(db.String)
    
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone', 'action')
        order = True
        