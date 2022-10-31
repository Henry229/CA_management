from flask import Blueprint, make_response, request, abort, redirect, url_for, render_template, flash
from init import db, bcrypt
from datetime import date, timedelta
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    # stmt = db.select(User)
    # users = db.session.scalars(stmt)
    return render_template('index.html')
    # return UserSchema(many=True, exclude=['password']).dump(users)  


# @auth_bp.route('/users/')
# def get_users():
#     stmt = db.select(User)
#     users = db.session.scalars(stmt)
#     return UserSchema(many=True, exclude=['password']).dump(users)    


@auth_bp.route('/login/', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        stmt = db.select(User).filter_by(email=request.form.get('email'))
        user = db.session.scalar(stmt)
    # If user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
            # headers = {'Authorization': 'Bearer {}'.format(access_token)}
            resp = make_response(redirect(url_for('employees.get_employee'))) 
            set_access_cookies(resp, access_token)
            return resp
            # JWT = access_token
            # login_id = get_jwt_identity()
            # print('#### yogida check :', login_id)
            # return redirect(url_for('employees.index'))
            # return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
        else:
            flash('Error: Invalid email or password')
            return redirect(url_for('auth.auth_login'))
            # return {'error': 'Invalid email or password'}, 401
    return redirect(url_for('auth.auth_login'))
    # return render_template("login.html")
    # return render_template("login.html", user=current_user)
    
@auth_bp.route('/signup/', methods=['GET','POST'])
def auth_signup():
    print('***yogida1', request)
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        stmt = db.select(User).filter_by(email=email)
        user = db.session.scalar(stmt)
        
        if user:
            flash('Email already exists')
        elif password1 != password2:
            flash('Password mismatch')
        else:
            try:
            # Create a new User model instance from the user_info
                user = User(
                    email = email,
                    name = name,
                    password = bcrypt.generate_password_hash(password1).decode('utf8'),
                    register_date = date.today()
                )
                # Add and commit user to DB
                db.session.add(user)
                db.session.commit()
                # Respond to client
                flash('Account created successfully!!')
                return redirect(url_for('auth.auth_login'))
            except IntegrityError:
                return {'error': 'Email address already in use'}, 409
        # return redirect(url_for('auth.auth_login'))
    return render_template("signup.html")

@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
def auth_logout():
    current_user = get_jwt_identity()
    resp = make_response(redirect(url_for('auth.index')))
    unset_jwt_cookies(resp)
    return resp


def authorize():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        abort(401)
        

@auth_bp.route('/register/', methods=['POST'])
def auth_register():
    try:
        # Create a new User model instance from the user_info
        user = User(
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
            name = request.json.get('name')
        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to client
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409
