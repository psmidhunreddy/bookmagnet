from .models import db,User,Books,BookIssue,Section
from matplotlib import pyplot
from datetime import datetime,timedelta
from sqlalchemy import and_,or_
import base64,io

def save_plot():
    buf=io.BytesIO()
    pyplot.savefig(buf, format='png')
    buf.seek(0)
    image=base64.b64encode(buf.getvalue()).decode('utf-8')
    pyplot.close()
    return image

def get_lastMonths_issuedBooks(uid):
    curmonth_firstday=datetime(datetime.now().year,datetime.now().month,1)
    lastmonth_lastday=curmonth_firstday-timedelta(days=1)
    lastmonth_firstday=datetime(lastmonth_lastday.year,lastmonth_lastday.month,1)
    books_issued=BookIssue.query.filter(and_(BookIssue.uid==uid,
                                        and_(BookIssue.issue_date>lastmonth_firstday,
                                                BookIssue.issue_date<lastmonth_lastday),
                                       or_(BookIssue.book_status==1,BookIssue.book_status==2))).all()
    books_returned=BookIssue.query.filter(and_(BookIssue.uid==uid,
                                        and_(BookIssue.return_date>lastmonth_firstday,
                                                BookIssue.return_date<lastmonth_lastday),
                                       or_(BookIssue.book_status==1,BookIssue.book_status==2))).all()
    
    books_details=[]
    for book in books_issued:
        book_del=Books.query.filter(Books.id==book.bid).one()
        if book_del not in books_details:
            books_details.append(book_del)
    sections_details={'None':0}
    for book in books_details:
        if book.section_id:
            sec_del=Section.query.filter(Section.id==book.section_id).one()
            if sec_del.s_name in sections_details:
                sections_details[sec_del.s_name]+=1
            else:
                sections_details[sec_del.s_name]=1
        else:
            sections_details['None']+=1
    return books_issued,books_details,sections_details,(len(books_issued),len(books_returned))

def user_report(uid):
    lastmonth_books,book_details,sections_details,(issue_count,return_count)=get_lastMonths_issuedBooks(uid)
    s_names=list(sections_details.keys())
    s_count=list(sections_details.values())
    pyplot.figure(figsize=(10,6))
    pyplot.bar(s_names,s_count,width = 0.4)
    pyplot.title("Books issued in each section(last month)")
    pyplot.xlabel('Section')
    pyplot.ylabel('No of books')
    section_graph=save_plot()
    pyplot.figure(figsize=(10,6))
    labels=['Issued Books','Return Books']
    counts=[issue_count,return_count]
    pyplot.bar(labels,counts,width = 0.4)
    pyplot.title("Books issued vs Books returned(last month)")
    pyplot.ylabel('No of books')
    book_graph=save_plot()
    #print(book_details)
    return lastmonth_books,book_details,sections_details,section_graph,book_graph