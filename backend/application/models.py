from datetime import datetime
from . import db
from flask_login import UserMixin
from pytz import timezone 

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id =db.Column(db.Integer, primary_key=True)
    stored_email =db.Column(db.String(64), unique=True, nullable=False)
    stored_name=db.Column(db.String(64))
    stored_username =db.Column(db.String(64), nullable=False)
    stored_password =db.Column(db.String(64), unique=True, nullable=False)
    last_visited =db.Column(db.DateTime(), default=datetime.now(timezone("Asia/Kolkata")))
    role = db.Column(db.String(32), nullable=False, default="user")
    stored_books=db.relationship('BookIssue', backref='user', cascade="all,delete")
    stored_rating=db.relationship('Rating', backref='user', cascade="all,delete")   
    count=db.Column(db.Integer,default=0)
    def to_dict(self):
        return{
            "id":self.id,
            "email":self.stored_email,
            "name":self.stored_name,
            "username":self.stored_username,
            "last_visited":self.last_visited,
            "role":self.role,
            "count":self.count,
            "stored_rating":[rate.to_dict() for rate in self.stored_rating]
        }
class Section(db.Model,UserMixin):
    __tablename__='section'
    id=db.Column(db.Integer,primary_key=True)
    s_name=db.Column(db.String(64), unique=True, nullable=False)
    description=db.Column(db.String(128))
    doc=db.Column(db.DateTime, default=datetime.now(timezone("Asia/Kolkata")))
    stored_books=db.relationship('Books', backref='section')
    def to_dict(self):
        return{
            "id":self.id,
            "s_name":self.s_name,
            "description":self.description,
            "stored_books":[sec.to_dict() for sec in self.stored_books],
            "doc":self.doc
        }

class Books(db.Model, UserMixin):
    __tablename__='books'
    id=db.Column(db.Integer,primary_key=True)
    b_name=db.Column(db.String(64), nullable=False)
    author_name=db.Column(db.String(64),nullable=False)
    b_photo=db.Column(db.String(64), default="/static/coverphotos/default.jpg")
    avail_status=db.Column(db.Integer,default=1)
    book_content=db.Column(db.String,default="/static/books/default.jpg")
    section_id=db.Column(db.Integer,db.ForeignKey('section.id'))
    stored_rating=db.relationship('Rating', backref='books', cascade="all,delete")
    stored_issues=db.relationship('BookIssue', backref='books', cascade="all,delete")
    def to_dict(self):
        return{
            "id":self.id,
            "bookname":self.b_name,
            "authorname":self.author_name,
            "b_photo":self.b_photo,
            "avail_status":self.avail_status,
            "book_content":self.book_content,
            "section_id":self.section_id,
            "rating":sum([rate.value for rate in self.stored_rating])/len(self.stored_rating) if len(self.stored_rating)>0 else 0
        }
class BookIssue(db.Model, UserMixin):
    __tablename__='bookissue'
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"))
    bid=db.Column(db.Integer,db.ForeignKey('books.id',ondelete="CASCADE"))
    issue_date=db.Column(db.DateTime)
    return_date=db.Column(db.DateTime)
    book_status=db.Column(db.Integer)

    def to_dict(self):
        return{
            "id":self.id,
            "uid":self.uid,
            "bid":self.bid,
            "bookdels":Books.query.get(self.bid).to_dict(),
            "issue_date":self.issue_date,
            "return_date":self.return_date,
            "book_status":self.book_status
        }

class Rating(db.Model,UserMixin):
    __tablename__='rating'
    id=db.Column(db.Integer,primary_key=True)
    value=db.Column(db.Integer)
    bid=db.Column(db.Integer, db.ForeignKey('books.id',ondelete="CASCADE"))
    uid=db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"))
    def to_dict(self):
        return{
            "id":self.id,
            "value":self.value,
            "bid":self.bid,
            "uid":self.uid
        }


