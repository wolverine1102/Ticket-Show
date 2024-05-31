from datetime import datetime
from flask import current_app as app
from flask import request, jsonify
from sqlalchemy import or_, and_
from flask_security import roles_accepted
from .models import *
from .validation import *
from .cache import cache
from .home import home_page


@app.route('/admin/dashboard/shows/')
@cache.memoize()
@roles_accepted('admin')
def admin_dashboard_shows():
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


@app.route('/admin/dashboard/shows/create', methods = ['POST'])
@roles_accepted('admin')
def admin_create_shows():
    data = request.json
    id = data['id']
    name = data['name']
    rating = data['rating']
    category = data['category']
    tags = data['tags']
    languages = data['languages']
    duration = data['duration']
    release_date = data['release_date']
    photo = data['photo']
    description = data['description']

    release_date = datetime.strptime(release_date, '%Y-%m-%d').date()

    show = Shows(id=id, name=name, rating=rating, category=category, tags=tags, languages=languages, 
                 duration=duration, release_date=release_date, description=description, photo=photo)
    try:
        db.session.add(show)
        db.session.commit()     
        cache.delete_memoized(admin_dashboard_shows)
        cache.delete_memoized(home_page)
    except:
        db.session.rollback()
        raise AlreadyExist(status_code=409, error_message='Show ID already exists')
    
    return 'Success', 200


@app.route('/admin/dashboard/shows/<show_id>/modify', methods = ['GET', 'POST'])
@roles_accepted('admin')
def admin_modify_shows(show_id):
    if request.method == 'GET':
        show = Shows.query.filter_by(id=show_id).first()
        show_dict = {'id' : show.id,
                     'name' : show.name, 
                     'rating' : show.rating,
                     'category' : show.category, 
                     'tags' : show.tags,
                     'languages' : show.languages, 
                     'duration' : show.duration,
                     'release_date' : show.release_date.strftime('%Y-%m-%d'), 
                     'description' : show.description, 
                     'photo' : show.photo}
        return jsonify(show_dict)
    
    elif request.method == 'POST':
        data = request.json
        name = data['name']
        rating = data['rating']
        category = data['category']
        tags = data['tags']
        languages = data['languages']
        duration = data['duration']
        release_date = data['release_date']
        description = data['description']
        photo = data['photo']

        release_date = datetime.strptime(release_date, '%Y-%m-%d').date()

        show = Shows.query.filter_by(id=show_id).first()
        show.name = name
        show.rating = rating
        show.category = category
        show.tags = tags
        show.languages = languages
        show.duration = duration
        show.release_date = release_date
        show.description = description
        show.photo = photo
        
        db.session.commit()
        cache.delete_memoized(admin_dashboard_shows)
        cache.delete_memoized(home_page)
        return 'Success', 200
    

@app.route('/admin/dashboard/shows/<show_id>/delete')
@roles_accepted('admin')
def admin_delete_shows(show_id):
    show = Shows.query.get(show_id)
    hosted_venues = Hosted_Shows.query.filter_by(show_id=show_id).all()
    if hosted_venues:
        for venue in hosted_venues:
            db.session.delete(venue)
            db.session.commit()
    db.session.delete(show)
    db.session.commit()
    cache.delete_memoized(admin_dashboard_shows)
    cache.delete_memoized(home_page)
    return 'Success', 200




   
