from flask_mail import Message
from app import mail
from threading import Thread
from flask import current_app

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def task_give_to_thread(subject, recipients, body, html=None):
    app=current_app._get_current_object()

    msg = Message(subject=subject, recipients=recipients)
    msg.body = body

    if html:
        msg.html = html

    thread = Thread(target=send_async_email, args=(app, msg))
    thread.start()
    return thread