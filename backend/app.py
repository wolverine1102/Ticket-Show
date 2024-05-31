from flask import Flask, render_template
from flask import request, jsonify
from datetime import datetime
from application.database import db
from application.cache import cache
from application.config import LocalDevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore, current_user, login_required, logout_user
from flask_security.utils import hash_password, verify_password, login_user
from application.models import Users, Roles
from flask_cors import CORS
from application.celery_worker import *

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = Security(app, user_datastore)
CORS(app)
celery = make_celery(app)
cache.init_app(app)

app.app_context().push()

from application.venues_controllers import *
from application.shows_controllers import *
from application.hosted_shows_controllers import *
from application.home import *
from application.book_ticket_controllers import *
from application.tasks import *
from application.daily_reminder import *
from application.monthly_report import *
from application.csv_report import *




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/user/create', methods=['POST'])
def create_account():
    data = request.json
    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']
    password = hash_password(data['password'])
    user_role = Roles.query.filter_by(name="user").first()
    user = Users.query.filter_by(email=email).first()
    if user:
        raise AlreadyExist(status_code=409, error_message='Email id already exists')
    else:
        user = user_datastore.create_user(email=email, 
                                      first_name=first_name, 
                                      last_name=last_name, 
                                      password=password)
    user.roles.append(user_role)
    db.session.commit()
    login_user(user)
    current_user.login_time = datetime.datetime.now()
    db.session.commit()
    return jsonify({'email' : current_user.email,
                    'first_name' : current_user.first_name,
                    'last_name' : current_user.last_name,
                    'roles' : [role.id for role in current_user.roles],
                    'token':current_user.get_auth_token()})
    

@app.route('/user/login', methods=['POST'])
def user_login():
    data = request.json
    email = data['email']
    password = data['password']
    admin = data['role']
    user = Users.query.filter_by(email=email).first()
    if not user or not (verify_password(password, user.password)):
        raise BusinessValidationError(status_code=401, error_message='Bad Credentials')
    
    elif admin and user and verify_password(password, user.password):
        roles = [role.id for role in user.roles]
        if 'admin' not in roles:
            raise BusinessValidationError(status_code=403, error_message='Forbidden')
        else:
            login_user(user)
            current_user.login_time = datetime.datetime.now()
            db.session.commit()
            return jsonify({'email' : current_user.email,
                            'first_name' : current_user.first_name,
                            'last_name' : current_user.last_name,
                            'roles' : [role.id for role in current_user.roles],
                            'token':current_user.get_auth_token()})
    
    else:
        login_user(user)
        current_user.login_time = datetime.datetime.now()
        db.session.commit()
        return jsonify({'email' : current_user.email,
                    'first_name' : current_user.first_name,
                    'last_name' : current_user.last_name,
                    'roles' : [role.id for role in current_user.roles],
                    'token':current_user.get_auth_token()})


@app.route('/user/logout')
@login_required
def user_logout():
    logout_user()
    return 'Success', 200


@app.route('/user/dashboard')
@login_required
def user_dashboard():
    name = current_user.first_name
    booked_shows = Booked_Shows.query.filter_by(user_email_id=current_user.email).all()
    shows = []
    for show in booked_shows:
        show_id = Hosted_Shows.query.get(show.hosted_show_id).show_id
        venue_id = Hosted_Shows.query.get(show.hosted_show_id).venue_id
        language = Hosted_Shows.query.get(show.hosted_show_id).language
        venue = Venues.query.get(venue_id)
        venue_name = venue.name + ', ' + venue.place + ', ' + venue.location + ', ' + venue.city
        date = show.date
        shows.append({'show' : Shows.query.get(show_id).name, 
                      'venue' : venue_name, 
                      'language' : language,
                      'timing' : Hosted_Shows.query.get(show.hosted_show_id).timing,
                      'date' : date.strftime("%A, %d %b, %Y"), 
                      'numOfSeats' : show.num_of_seats})
    return jsonify({
        'bookedShowsList' : shows
    })




if __name__ == '__main__':
    # Run Flask app
    app.run(
        host = '0.0.0.0',
        debug = True
    )