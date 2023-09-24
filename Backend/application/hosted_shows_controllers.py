from datetime import datetime
from flask import current_app as app
from flask import request, jsonify
from sqlalchemy import or_, and_
from flask_security import roles_accepted
from .models import *
from .validation import *
from .cache import cache


@app.route('/admin/dashboard/shows/<show_id>/venues')
@cache.memoize()
@roles_accepted('admin')
def admin_shows_hosting_venues(show_id):
    hosting_venues = Hosted_Shows.query.filter_by(show_id=show_id).all()
    venue_dict = None
    if hosting_venues:
        venue_dict = []
        for venue in hosting_venues:
            venue_name = Venues.query.get(venue.venue_id)
            venue_dict.append({'name' : venue_name.name, 
                               'timing' : venue.timing, 
                               'ticketPrice' : venue.ticket_price,
                               'language' : venue.language, 
                               'startDate' : venue.start_date.strftime("%d %b, %Y"), 
                               'endDate' : venue.end_date.strftime("%d %b, %Y"),
                               'id' : venue.id})
        
    return jsonify(venue_dict)


@app.route('/admin/dashboard/shows/<show_id>/add_venue', methods = ['GET', 'POST'])
@roles_accepted('admin')
def admin_shows_add_venues(show_id):
    if request.method == 'GET':
        venues = Venues.query.all()
        show = Shows.query.get(show_id)
        languages = show.languages.split(',')
        venue_list = []
        for venue in venues:
            venue_list.append({
                'id' : venue.id,
                'name' : venue.name
            })
        
        return jsonify({
            'venues' : venue_list,
            'languages' : languages,
            'releaseDate' : show.release_date.strftime('%Y-%m-%d')
        })
    
    elif request.method == 'POST':
        data = request.json
        show_id = show_id
        venue_id = data['venue_id']
        ticket_price = data['ticket_price']
        language = data['language']
        timing = data['timing']
        start_date = data['start_date']
        end_date = data['end_date']
        id = show_id + '-' + venue_id + '-' + timing
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        hosted_show = Hosted_Shows(id=id, show_id=show_id, venue_id=venue_id, timing=timing, ticket_price=ticket_price,
                                   language=language, start_date=start_date, end_date=end_date)
        
        already_added_show = Hosted_Shows.query.get(id)
        if already_added_show:
            raise AlreadyExist(status_code=409, error_message='This show already exists')
        else:
            db.session.add(hosted_show)
            db.session.commit()
            cache.delete_memoized(admin_shows_hosting_venues)
        
        return 'Success', 200
    

@app.route('/admin/dashboard/shows/<id>/modify_venue', methods=['GET', 'POST'])
@roles_accepted('admin')
def admin_shows_modify_hosting_venue(id):
    if request.method == 'GET':
        hosted_venue = Hosted_Shows.query.get(id)
        venue_id = Venues.query.filter_by(id=hosted_venue.venue_id).first().id
        venue_name = Venues.query.filter_by(id=hosted_venue.venue_id).first().name
        show = Shows.query.filter_by(id=hosted_venue.show_id).first()
        languages = show.languages.split(',')
    
        return jsonify ({
            'venueId' : venue_id,
            'name' : venue_name,
            'languageList' : languages,
            'releaseDate' : show.release_date.strftime('%Y-%m-%d'),
            'timing' : hosted_venue.timing,
            'ticketPrice' : hosted_venue.ticket_price,
            'language' : hosted_venue.language,
            'startDate' : hosted_venue.start_date.strftime('%Y-%m-%d'),
            'endDate' : hosted_venue.end_date.strftime('%Y-%m-%d'),
            'showId' : show.id
        })
    
    elif request.method == 'POST':
        data = request.json
        ticket_price = data['ticket_price']
        language = data['language']
        start_date = data['start_date']
        end_date = data['end_date']
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        hosted_show = Hosted_Shows.query.get(id)
        hosted_show.ticket_price = ticket_price
        hosted_show.language = language
        hosted_show.start_date = start_date
        hosted_show.end_date = end_date
        db.session.commit()
        cache.delete_memoized(admin_shows_hosting_venues)

        return 'Success', 200
    

@app.route('/admin/dashboard/shows/<id>/delete_venue')
@roles_accepted('admin')
def admin_shows_delete_hosting_venue(id):
    hosted_venue = Hosted_Shows.query.get(id)
    show_id = hosted_venue.show_id
    db.session.delete(hosted_venue)
    db.session.commit()
    cache.delete_memoized(admin_shows_hosting_venues)

    return 'Success', 200
        