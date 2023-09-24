from .database import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('Roles_Users',
        db.Column('user_id', db.Integer(), db.ForeignKey('Users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('Roles.id'))) 

class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean)
    login_time = db.Column(db.DateTime, nullable=False)
    roles = db.relationship('Roles', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Roles(db.Model, RoleMixin):
    __tablename__ = 'Roles'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)

class Venues(db.Model):
    __tablename__= 'Venues'
    id = db.Column(db.String, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    place = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    available_facilities = db.Column(db.String)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Shows', secondary='Hosted_Shows', back_populates='venues')

class Shows(db.Model):
    __tablename__ = 'Shows'
    id = db.Column(db.String, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    rating = db.Column(db.String)
    category = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)
    languages = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String)
    photo = db.Column(db.String)
    venues = db.relationship('Venues', secondary='Hosted_Shows', back_populates='shows')

class Hosted_Shows(db.Model):
    __tablename__ = 'Hosted_Shows'
    id = db.Column(db.String, primary_key=True, nullable=False)
    show_id = db.Column(db.String, db.ForeignKey('Shows.id'), nullable=False)
    venue_id = db.Column(db.String, db.ForeignKey('Venues.id'), nullable=False)
    timing = db.Column(db.String, nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

class Booked_Shows(db.Model):
    __tablename__ = 'Booked_Shows'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    hosted_show_id = db.Column(db.String, db.ForeignKey('Hosted_Shows.id'), nullable=False)
    user_email_id = db.Column(db.String, db.ForeignKey('Users.email'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    num_of_seats = db.Column(db.Integer, nullable=False)