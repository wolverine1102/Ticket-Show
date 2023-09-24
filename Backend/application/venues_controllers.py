from flask import current_app as app
from flask import request, jsonify
from sqlalchemy import or_, and_
from flask_security import roles_accepted
from .models import *
from .validation import *
from .cache import cache


@app.route('/admin/dashboard/venues/')
@cache.memoize()
@roles_accepted('admin')
def admin_dashboard_venues():
    venueList = None
    venues = Venues.query.all()
    if venues:
        venueList = []
        for venue in venues:
            venueList.append({
                'id': venue.id,
                'name': venue.name,
                'place': venue.place,
                'location': venue.location,
                'city': venue.city,
                'state': venue.state,
                'available_facilities': venue.available_facilities,
                'capacity': venue.capacity
            })
    return jsonify(venueList)


@app.route('/admin/dashboard/venues/create', methods = ['POST'])
@roles_accepted('admin')
def admin_create_venues():
    data = request.json
    id = data['id']
    name = data['name']
    place = data['place']
    location = data['location']
    city = data['city']
    state = data['state']
    available_facilities = data['available_facilities']
    capacity = data['capacity']
    venue = Venues(id=id, name=name, place=place, location=location, city=city, state=state, 
    available_facilities=available_facilities, capacity=capacity)
    try:
        db.session.add(venue)
        db.session.commit()     
        cache.delete_memoized(admin_dashboard_venues)
    except:
        db.session.rollback()
        raise AlreadyExist(status_code=409, error_message='Venue ID already exists')
    
    return 'Success', 200


@app.route('/admin/dashboard/venues/<venue_id>/modify', methods = ['GET', 'POST'])
@roles_accepted('admin')
def admin_modify_venues(venue_id):
    if request.method == 'GET':
        venue = Venues.query.filter_by(id=venue_id).first()
        venue_dict = {'id' : venue.id,
                      'name' : venue.name, 
                      'place' : venue.place,
                      'location' : venue.location,
                      'city' : venue.city,
                      'state' : venue.state,
                      'available_facilities' : venue.available_facilities,
                      'capacity' : venue.capacity}
        return jsonify(venue_dict)
    
    elif request.method == 'POST':
        data = request.json
        name = data['name']
        place = data['place']
        location = data['location']
        city = data['city']
        state = data['state']
        available_facilities = data['available_facilities']
        capacity = data['capacity']

        venue = Venues.query.filter_by(id=venue_id).first()
        venue.name = name
        venue.place = place
        venue.location = location
        venue.city = city
        venue.state = state
        venue.available_facilities = available_facilities
        venue.capacity = capacity
        
        db.session.commit()
        cache.delete_memoized(admin_dashboard_venues)
        return 'Success', 200
    

@app.route('/admin/dashboard/venues/<venue_id>/delete')
@roles_accepted('admin')
def admin_delete_venues(venue_id):
    venue = Venues.query.filter_by(id=venue_id).first()
    hosted_shows = Hosted_Shows.query.filter_by(venue_id=venue_id)
    if hosted_shows:
        for show in hosted_shows:
            db.session.delete(show)
            db.session.commit()
    db.session.delete(venue)
    db.session.commit()
    cache.delete_memoized(admin_dashboard_venues)
    return 'Success', 200

    
    