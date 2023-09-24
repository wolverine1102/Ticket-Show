from celery.schedules import crontab
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from .models import *
from .tasks import celery
from jinja2 import Template
from weasyprint import HTML, CSS


SMTP_SERVER_HOST = 'localhost'
SMTP_SERVER_PORT = '1025'
SENDER_ADDRESS = 'info@ticketshow.com'
SENDER_PASSWORD = ''


def send_monthly_report(to, subject, message):
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    with open('static/Your Monthly Report.pdf', 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    
    encode_base64(part)
    part.add_header(
        'Content-Disposition', 'attachment; filename=Your Monthly Report.pdf',
    )
    msg.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST,
                     port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True


def generate_monthly_report(user):
    with open('templates/monthly_report.html') as report:
        template = Template(report.read())
        booked_shows = Booked_Shows.query.filter_by(user_email_id=user.email).all()
        shows = []
        first = datetime.date.today().replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        for show in booked_shows:
            show_id = Hosted_Shows.query.get(show.hosted_show_id).show_id
            venue_id = Hosted_Shows.query.get(show.hosted_show_id).venue_id
            language = Hosted_Shows.query.get(show.hosted_show_id).language
            venue = Venues.query.get(venue_id)
            venue_name = venue.name + ', ' + venue.place + ', ' + venue.location + ', ' + venue.city
            date = show.date
            if date.strftime('%b') == last_month.strftime('%b'):
                shows.append({'show' : Shows.query.get(show_id).name, 
                            'language' : language,
                            'venue' : venue_name, 
                            'timing' : Hosted_Shows.query.get(show.hosted_show_id).timing,
                            'date' : date.strftime("%A, %d %b, %Y"), 
                            'numOfSeats' : show.num_of_seats})
            
        return template.render(user=user, shows=shows)
    

def convert_to_pdf(user):
    report = generate_monthly_report(user)
    html_report = HTML(string=report, base_url='')
    html_report.write_pdf('static/Your Monthly Report.pdf')
    


@celery.task
def main():
    users = Users.query.all()
    if users:
        for user in users:
            message = generate_monthly_report(user)
            convert_to_pdf(user)
            send_monthly_report(to=user.email, 
                                subject="Monthly Report", 
                                message=message)
            
        return "Monthly Report will be sent shortly..."


@celery.on_after_configure.connect
def setup_monthly_report(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=14, minute=12),
        main.s(),
    )


if __name__ == '__main__':
    main()



