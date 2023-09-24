import csv
import time
from zipfile import ZipFile
from flask import current_app as app
from flask import jsonify, send_file
from flask_security import roles_accepted
from .models import *
from .tasks import celery


@app.route('/export_csv')
@roles_accepted('admin')
def export_csv():
    task = generate_csv.delay()
    task.wait()
    return jsonify({
            'state' : task.state
        })


@app.route('/download')
def download():
    venues = Venues.query.all()
    if venues:
        with ZipFile('static/csv_report/Venues.zip','w') as zip:
            for venue in venues:
                name = venue.name.split(':')
                filename = name[0] + ' -' + name[-1] + '.csv'
                zip.write('static/csv_report/' + filename)
        return send_file('static/csv_report/Venues.zip')
    


@celery.task
def generate_csv():
    venues = Venues.query.all()
    if venues:
        for venue in venues:
            name = venue.name.split(':')
            filename = name[0] + ' -' + name[-1] + '.csv'
            fields = ['Capacity', 'No. of Shows', 'No. of Bookings', 'Seats Booked']
            capacity = venue.capacity
            no_of_shows = Hosted_Shows.query.filter_by(venue_id=venue.id).count()
            booked_shows = Booked_Shows.query.filter(Booked_Shows.hosted_show_id.ilike('%' + venue.id + '%'))
            no_of_bookings = booked_shows.count()
            seats_booked = 0
            for booked_show in booked_shows:
                seats_booked += booked_show.num_of_seats

            row = [[capacity, no_of_shows, no_of_bookings, seats_booked]]

            with open('static/csv_report/' + filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(fields)
                csvwriter.writerows(row)

            time.sleep(1)

    return True