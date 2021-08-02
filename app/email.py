from flask_mail import Message
from app import app, mail, celery
from flask import render_template

def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)



@celery.task
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[T-minus Showtime] Reset your password',
                sender=app.config['ADMINS'][0],
                recipients=[user.email],
                html_body=render_template('email/reset_password.html', user=user, token=token))

#TEST

def send_notification_emails(a_list):
    user_email = "mandylmoore45@gmail.com"
    send_email('[T-minus Showtime] New episodes tomorrow!',
            sender = app.config.get("MAIL_USERNAME"),
            recipients=[user_email],
            html_body=render_template('email/notification_new_eps.html', a_list=a_list))



