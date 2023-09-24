from flask import current_app as app
from flask import request, jsonify
from sqlalchemy import or_, and_
from .models import *
from .cache import cache


@app.route('/home/')
@cache.memoize()
def home_page():
    showList = None
    shows = Shows.query.all()
    if shows:
        showList = []
        for show in shows:
            showList.append({
                'id' : show.id,
                'name' : show.name,
                'rating' : show.rating,
                'category' : show.category,
                'tags' : show.tags,
                'languages' : show.languages,
                'duration' : show.duration,
                'release_date' : show.release_date.strftime("%d %b, %Y"),
                'description' : show.description,
                'photo' : show.photo
            })
    return jsonify(showList)


@app.route('/search/<keyword>/')
@cache.memoize()
def search(keyword):
    showList = None
    venueList = None
    venues = Venues.query.filter(or_(Venues.location.ilike('%' + keyword + '%'),
                                     Venues.place.ilike('%' + keyword + '%'),
                                     Venues.name.ilike('%' + keyword + '%'),
                                     Venues.city.ilike('%' + keyword + '%'))).all()
    shows = Shows.query.filter(or_(Shows.name.ilike('%' + keyword + '%'),
                                   Shows.tags.ilike('%' + keyword + '%'),
                                   Shows.languages.ilike('%' + keyword + '%'),
                                   Shows.rating.ilike(keyword + '%'))).all()
    if shows:
        showList = []
        for show in shows:
            showList.append({
                'id' : show.id,
                'name' : show.name,
                'rating' : show.rating,
                'category' : show.category,
                'tags' : show.tags,
                'languages' : show.languages,
                'duration' : show.duration,
                'release_date' : show.release_date.strftime("%d %b, %Y"),
                'description' : show.description,
                'photo' : show.photo
            })
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
            })
    return jsonify({
        'shows' : showList,
        'venues' : venueList,
    })


@app.route('/venues/<venue_name>')
@cache.memoize()
def venue_page(venue_name):
    showList = None
    venue = Venues.query.filter_by(name=venue_name).first()
    hosted_shows = Hosted_Shows.query.filter_by(venue_id=venue.id).all()
    if hosted_shows:
        showList = []
        for hosted_show in hosted_shows:
            show = Shows.query.get(hosted_show.show_id)
            if show.name not in showList:
                showList.append(show.name)
    venue_dict = {'id': venue.id,
                'name': venue.name,
                'place': venue.place,
                'location': venue.location,
                'availableFacilities': venue.available_facilities,
                'city': venue.city,
                'state': venue.state,}
    return jsonify({
        'shows' : showList,
        'venues' : venue_dict,
    })

