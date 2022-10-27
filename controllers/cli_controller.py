from flask import Blueprint
from init import db, ma 
from models.employee import Employee

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Talbes create successfully')

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Talbes dropped successfully')


