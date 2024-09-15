from celery import shared_task
from .models import User,BookIssue,Books,db
#import datetime
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
from flask import current_app
from .mail_service import send_message
from jinja2 import Template
from .user_monthly_report import user_report
from sqlalchemy import and_

@shared_task(ignore_result=False)
def daily_remainders():
    users=User.query.filter(User.role=='user').all()
    today = datetime.now().date()
    #send_message(to='midhunmgit@gmail.com',subject='Test', content_body='Test')
    #return "Success"
    for user in users:
        last_visit=user.last_visited.date()
        if today!=last_visit:
            f=open('dialy_remainder.html','r')
            t=Template(f.read())
            send_message(user.stored_email,"BookMagnet : Daily Remainder",t.render(user_details=user))
    return "Success"

@shared_task(ignore_result=False)
def monthly_remainders():
    users=User.query.filter(User.role=='user').all()
    for user in users:
        f=open('monthly_reports.html','r')
        t=Template(f.read())
        lastmonth_books,book_details,sections_details,section_graph,book_graph=user_report(user.id)
        send_message(user.stored_email,"BookMagnet : Monthly Report",
            t.render(user_details=user,lastmonth_books=lastmonth_books,book_details=book_details,
                sections_details=sections_details,section_graph=section_graph,book_graph=book_graph))
    return "Success"

@shared_task(ignore_result=False)
def revoke_overdues():
    overdues=BookIssue.query.filter(and_(BookIssue.book_status==1,datetime.now()>BookIssue.return_date)).all()
    for od in overdues:
        od.book_status=2
        od.return_date=datetime.now()
        user=User.query.filter(User.id==od.uid).one()
        user.count-=1
        book=Books.query.filter(Books.id==od.bid).one()
        book.avail_status=1
        db.session.commit()
    return "Success"

@shared_task(ignore_result=False)
def register_reply(uid):
    user=User.query.filter(User.id==uid).one()
    send_message(user.stored_email,"Sign Up Successfull - BookMagnet",
                 "<html><img src='https://i.ibb.co/VYNj5Mw/header.png' alt='header' border='0'><p>Hey <b>{}<b>, thanks for registering with us.</p><p>Don't forget to visit us</p><i>Happy Reading</i><br><p>Team BookMagnet</p></html>".format(user.stored_name))
    return "success"

@shared_task(ignore_result=False)
def passwordchange_reply(uid):
    user=User.query.filter(User.id==uid).one()
    send_message(user.stored_email,"Password Changed - BookMagnet",
                 "<html><img src='https://i.ibb.co/VYNj5Mw/header.png' alt='header' border='0'><p>Hello <b>{}<b>, your BookMagnet account password has been changed.Report immediately if not done</p><i>Happy Reading</i><br><p>Team BookMagnet</p></html>".format(user.stored_name))
    return "success"
