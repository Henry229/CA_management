from flask import Blueprint, render_template, redirect, url_for, request, flash 
from init import db, ma 
from models.employee import Employee, EmployeeSchema


employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/')
def index():
    stmt = db.select(Employee).order_by(Employee.id.asc())
    employees = db.session.scalars(stmt)
    return render_template('index.html', employees=employees)
  
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
            
            return redirect(url_for('employees.index'))

  
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
        
        return redirect(url_for('employees.index'))
      
@employees_bp.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    print('***yogida1')
    stmt = db.select(Employee).filter_by(id = id)
    employee = db.session.scalar(stmt)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!')
        return redirect(url_for('employees.index'))
    else:
        return {'error': f'Card not found with id {id}'}, 404
        