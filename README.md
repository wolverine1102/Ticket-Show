# Ticket-Show

Modern Application Development II - Project

**Description**

It’s a multi-user application for booking show tickets. We need to implement a login system
for both admin and user, a venue and show management system which will only be handled
by the admin and a booking tickets system for the user. We also need to implement background jobs –
for exporting, reporting and alerting. Also add caching support to improve API performance.

**Technologies used**
* Flask for API
* Vue 3 for UI
* Bootstrap for CSS
* SQLite for data storage
* Flask-Security for role-based access control
* Flask-SQLAlchemy for supporting SQLALchemy in the application
* Flask-Caching for caching support
* Redis for caching
* Redis and Celery for batch jobs

**DB Schema Design**

1. Users –
   * Columns – id, email, first_name, last_name, password, fs_uniquifier, login_time, roles.
   * id is the primary key for the table.
   * email stores email id for both admin and users.
   * password is first hashed using bcrypt and then stored in database.
   * fs_uniquifier is used to generate authentication tokens after a successful call to an authentication endpoint.
   * login_time is used to store a user’s latest login date and time. This is used for determining whether a user will be sent a daily reminder.
   * roles = db.relationship('Roles', secondary=roles_users)

2. Roles –
   * Columns – id, name.
   * id is the primary key for the table.
   * name stores name of the role – ‘user’ and ‘admin’.
  
3. Roles_Users –
   * Columns – user_id, role_id.
   * This table is used for role-based access control.
   * user_id and role_id are foreign keys which refers to Users.id and Roles.id respectively.

4. Venues -
   * Columns – id, name, place, location, city, state, available_facilities, capacity, shows.
   * id is the primary key for the table, which will be provided by the admin while creating new venues.
   * capacity will help to implement ability to stop taking bookings in case of a houseful.
   * shows = db. relationship (‘Shows’, secondary=’Hosted_Shows’)

5. Shows –
   * Columns – id, name, rating, category, tags, languages, duration, release_date, description, photo, venues.
   * id is the primary key for the table, which will be provided by the admin while creating new shows.
   * category determines whether a show is a movie or an event.
   * photo stores the link to the poster for the show.
   * venues = db. relationship (‘Venues’, secondary=’Hosted_Shows’)

6. Hosted_Shows –
   * Columns – id, show_id, venue_id, timing, ticket_price, language, start_date, end_date, seats_booked.
   * This tables holds information about where a show is being hosted, in which language and is maintained by the admin.
   * id is the primary key for the table, which is in format - "show_id-venue_id-timing".
   * start_date and end_date indicates the duration (in days) for which the show is being hosted. This will help the user to choose, from available dates to book the tickets.
   * show_id and venue_id are foreign keys which refers to Shows.id and Venues.id respectively.
  
7. Booked_Shows –
   * Columns – id, hosted_show_id, user_email_id, date, num_of_seats.
   * The table holds information about the particulars of the ticket booked by the user.
   * hosted_show_id and user_email_id are foreign keys which refers to Hosted_Shows.id and Persons.email_id respectively.

**API Design**

APIs has been created using Flask, which is accessed by Vue to display data on webpage. Few APIs are
protected using token-based authentication, from which some are protected using role-based access.

**Architecture and Features**

The SQLite database is stored in '/Backend/instance' folder and all the Vue.js files are in '/Frontend'. The model and
controllers are stored in ‘application’, which is accessed by app.py. Vue is launched using index.html which
is rendered from Flask app. Under ‘template’ index.html and monthly_report.html – which is used for
sending monthly report - is stored.
Both admin and user can login using email id and password, if the user doesn’t have an existing
account, he/she can create one. From admin dashboard, the admin can manipulate the Venues, Shows and
Hosted_Shows tables. User cannot access admin dashboard, Vue blocks the navigation to admin dashboard
and if attempted to access it from third-party app such as Postman, flask server will throw 403 error.
The home page of the application displays details of all the shows for the user, from where he/she can
proceed to book for a particular show. Before proceeding for booking, the user has to login or create an
account. User can also search for shows and venues using appropriate keywords. From user dashboard, user can see the list of all the bookings.
To book for a particular show, user has to first select the date of his/her preference. Then a list of all the
venues for the provided date are displayed, with different timings and languages. If a venue has reached
its maximum capacity for a specific timing, the user can no longer book it, the booking button gets disabled.
From user dashboard, an admin can export CSV files for each venue, this feature is disabled for user.
Daily reminders are sent to users if they have not logged in for more than 24hrs. Monthly reports of users’
bookings of last month are sent using email on second day of each month, the user can also download this
report in PDF format.
