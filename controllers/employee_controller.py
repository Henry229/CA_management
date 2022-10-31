from flask import Blueprint, render_template, redirect, url_for, request, flash 
from init import db, ma 
from models.employee import Employee, EmployeeSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


employees_bp = Blueprint('employees', __name__, url_prefix='/employees')

@employees_bp.route('/', methods=['GET', 'POST'])
@jwt_required()
def get_employee():
    login_id = get_jwt_identity()
    print (' login id : ', login_id)
    if login_id:
        stmt = db.select(Employee).order_by(Employee.id.asc())
        employees = db.session.scalars(stmt)
        return render_template('employee.html', employees=employees)
    else:
        return render_template('index.html')
  
@employees_bp.route('/update/', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        stmt = db.select(Employee).filter_by(id= request.form.get('id'))
        employee = db.session.scalar(stmt)
        if employee:
            employee.name = request.form['name']
            employee.email = request.form['email']
            employee.phone = request.form['phone']
            db.session.commit()
            flash("Employee updated successfully!")
            
            return redirect(url_for('employees.employee'))

  
@employees_bp.route('/insert/', methods=['POST'])
def insert():
    if request.method == 'POST':
        employee = Employee(
            name = request.form['name'],
            email = request.form['email'],
            phone = request.form['phone']
        )
        
        db.session.add(employee)
        db.session.commit()
        
        flash('Employee inserted successfully!')
        
        return redirect(url_for('employees.get_employee'))
      
@employees_bp.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    stmt = db.select(Employee).filter_by(id = id)
    employee = db.session.scalar(stmt)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!')
        return redirect(url_for('employees.employee'))
    else:
        return {'error': f'Card not found with id {id}'}, 404
        