from flask import current_app as app
from flask import request, jsonify
from sqlalchemy import or_, and_
from flask_security import login_required
from datetime import datetime
from .models import *
from .validation import *


@app.route('/book_ticket/<show_name>', methods=['GET', 'POST'])
@login_required
def book_ticket(show_name):
    if request.method == 'GET':
        show = Shows.query.filter_by(name=show_name).first()
        hosted_shows = Hosted_Shows.query.filter_by(show_id=show.id).all()
        if hosted_shows: 
            dates = sorted([shows.end_date for shows in hosted_shows])
            return jsonify({
                'startDate' : show.release_date.strftime('%Y-%m-%d'),
                'endDate' : dates[-1].strftime('%Y-%m-%d')
            })
        else:
            return jsonify({
                'startDate' : show.release_date.strftime('%Y-%m-%d'),
                'endDate' : show.release_date.strftime('%Y-%m-%d')
            })
    
    elif request.method == 'POST':
        show = Shows.query.filter_by(name=show_name).first()
        data = request.json
        date = data['date']
        date = datetime.strptime(date, '%Y-%m-%d').date()
        hosted_shows = Hosted_Shows.query.filter(Hosted_Shows.show_id == show.id, 
                                                 Hosted_Shows.start_date <= date, 
                                                 Hosted_Shows.end_date >= date).order_by(Hosted_Shows.venue_id).all()
        venue_dict = {}
        venue_names = []
        if hosted_shows: 
            for show in hosted_shows:
                if show.venue_id in venue_dict.keys():
                    seats_booked = 0
                    same_day_shows = Booked_Shows.query.filter(and_(Booked_Shows.hosted_show_id==show.id, 
                                                                    Booked_Shows.date==date)).all()
                    if same_day_shows:
                        for same_show in same_day_shows:
                            seats_booked += same_show.num_of_seats
                    capacity = Venues.query.filter_by(id=show.venue_id).first().capacity
                    available_seats = int(capacity) - seats_booked
                    venue_dict[show.venue_id].append({'language' : show.language, 
                                                      'timing' : show.timing,
                                                      'showId' : show.id, 
                                                      'availableSeats' : available_seats,
                                                    })
                else:
                    venue_dict[show.venue_id] = []
                    seats_booked = 0
                    same_day_shows = Booked_Shows.query.filter(and_(Booked_Shows.hosted_show_id==show.id, 
                                                                    Booked_Shows.date==date)).all()
                    if same_day_shows:
                        for same_show in same_day_shows:
                            seats_booked += same_show.num_of_seats
                    capacity = Venues.query.filter_by(id=show.venue_id).first().capacity
                    available_seats = int(capacity) - seats_booked
                    venue_dict[show.venue_id].append({'language' : show.language, 
                                                      'timing' : show.timing,
                                                      'showId' : show.id, 
                                                      'availableSeats' : available_seats,
                                                    })
            
            
            for venue_id in venue_dict.keys():
                venue_names.append(Venues.query.get(venue_id).name)

        return jsonify({
            'venueDict' : venue_dict,
            'venueList' : venue_names,
            'showDate' : date.strftime("%d %b, %Y")
        })
        

@app.route('/book_ticket/<show_name>/<date>/<hosted_show_id>', methods=['GET', 'POST'])
@login_required
def book_ticket_confirmation(show_name, date, hosted_show_id):
    seats_booked = 0
    same_day_shows = Booked_Shows.query.filter(and_(Booked_Shows.hosted_show_id==hosted_show_id, 
                                                    Booked_Shows.date==date)).all()
    if same_day_shows:
        for show in same_day_shows:
            seats_booked += show.num_of_seats

    if request.method == 'GET':
        show_name = show_name
        hosted_show = Hosted_Shows.query.get(hosted_show_id)
        venue = Venues.query.get(hosted_show.venue_id)
        date = datetime.strptime(date, '%Y-%m-%d').date()
        return jsonify({
            'venueName' : venue.name,
            'timing' : hosted_show.timing,
            'availableSeats' : int(venue.capacity) - seats_booked,
            'price' : hosted_show.ticket_price,
            'language' : hosted_show.language
        })
    
    elif request.method == 'POST':
        data = request.json
        num_of_seats = int(data['num_of_seats'])
        hosted_show = Hosted_Shows.query.get(hosted_show_id)
        venue = Venues.query.get(hosted_show.venue_id)
        available_seats = int(venue.capacity) - seats_booked
        if num_of_seats > available_seats:
            raise BusinessValidationError(status_code=403, error_message='Invalid Number of Seats')
        else:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            user_email = data['email_id']
            booked_show = Booked_Shows(hosted_show_id=hosted_show_id, user_email_id=user_email, date=date,
                                       num_of_seats=num_of_seats)
            db.session.add(booked_show)
            db.session.commit()
            return 'Success', 200