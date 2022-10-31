from flask import Flask
from init import db, ma, bcrypt, jwt 
from controllers.employee_controller import employees_bp
from controllers.auth_controller import auth_bp
from controllers.cli_controller import db_commands
import os


def create_app():
    
    app = Flask(__name__)

    app.config['JSON_SORT_KEY'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    # app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_CSRF_CHECK_FORM'] = True
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    app.register_blueprint(employees_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands)

    # return render_template('index.html')
    return app
  
  