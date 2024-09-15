from flask import Blueprint,request, redirect, flash, url_for, session,Response, jsonify
from flask import render_template,send_file
from flask_login import login_required, current_user
from . import db
from .models import User,Section,Books,BookIssue,Rating
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
import os
from werkzeug.utils import secure_filename
from datetime import date,timedelta, datetime
from sqlalchemy import or_,and_
from pytz import timezone
from .tasks import register_reply,passwordchange_reply
myapplication=Blueprint('apps',__name__)

def allow_imagefile(filename):
    ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
def allow_pdffile(filename):
    ALLOWED_EXTENSION = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@myapplication.route("/")
def home():
    return "Hello"

@myapplication.route("/register",methods=['POST','GET'])
def register():
    data=request.get_json()
    email=data.get('email')
    username=data.get('username')
    password=data.get('password')
    name=data.get('name')
    role='user'
    if not email or not username or not password:
        return jsonify({'msg':'REQUIRED FIELDS CAN\'T BE EMPTY'}), 409
    existing_user = User.query.filter_by(stored_email=email).first()
    existing_username=User.query.filter_by(stored_username=username).first()
    if existing_user:
        return jsonify({'msg':'Email is already Registered'}), 409
    if existing_username:
        return jsonify({'msg': 'Username already exist'}),409
        
    new_user=User(stored_email=email,stored_name=name,stored_username=username,stored_password=generate_password_hash(password),role=role)
    try:
        db.session.add(new_user)
        
        db.session.commit()
        x=register_reply(new_user.id)
        return jsonify({'msg':'Registration Successful.Please Login'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg':f'Some error occured {str(e)}'}), 409


@myapplication.route("/login",methods=["GET","POST"])
def login():
    data=request.get_json()
    username=data.get('username')
    password=data.get('password')
    if not username or not password:
        return jsonify({'msg':'REQUIRED FIELDS CAN\'T BE EMPTY'}), 409
    user_exist=User.query.filter_by(stored_username=username).first()
    if not user_exist:
        return jsonify({'msg':'Username not found'}),409
    if not check_password_hash(user_exist.stored_password,password):
        return jsonify({'msg':'Password incorrect'}),409
    access_token=create_access_token(identity={'id':user_exist.id})
    last_vist=user_exist.last_visited.strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({'msg':'Login Successful','access_token':access_token,'user':user_exist.to_dict(),'last_visit':last_vist}),201



@myapplication.route("/addbook",methods=["post"])
@jwt_required()
def addbook():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role != 'admin':
        return jsonify({'msg':'Access denied. Only librarian can add books'}),403
    bookname=request.form.get("bookname")
    authorname=request.form.get("authorname")
    file1=request.files['file1']
    file2=request.files['file2']
    if not file1 or not file2 or not bookname or not authorname:
        return jsonify({"msg":"Give all fields mentioned"}),409
    if not allow_pdffile(file1.filename):
        return jsonify({"msg":"Upload books of Pdf format only"}),409
    if not allow_imagefile(file2.filename):
        return jsonify({"msg":"Upload coverphoto of jpg/png format only"}),409
    book_filename="book_"+secure_filename(bookname)+file1.filename
    coverphoto_filename="cv_"+secure_filename(bookname)+file2.filename
    input_book="books/"+book_filename
    input_cover="coverphotos/"+coverphoto_filename
    new_book=Books(b_name=bookname,author_name=authorname,b_photo=input_cover,book_content=input_book)
    file1.save(os.path.join(myapplication.root_path,'../../frontend/public/books/',book_filename))
    file2.save(os.path.join(myapplication.root_path,'../../frontend/public/coverphotos/',coverphoto_filename))
    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'msg':'Book added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg':f'Some error occured {str(e)}'}),409
    
@myapplication.route("/getbooks",methods=["GET"])
@jwt_required()
def getbooks():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role =='admin':
        books=Books.query.all()
        input_data=[]
        for book in books:
            ib0=BookIssue.query.filter(BookIssue.bid==book.id,BookIssue.book_status==0).one_or_none()
            ib1=BookIssue.query.filter(BookIssue.bid==book.id,BookIssue.book_status==1).one_or_none()
            if ib0:
                u=User.query.filter(User.id==ib0.uid).one()
                d={'id':book.id,'bookname':book.b_name,'section_id':book.section_id,'authorname':book.author_name,'coverphoto':book.b_photo,'username':u.stored_username,'email':u.stored_email,'type':'req'}
            elif ib1:
                u=User.query.filter(User.id==ib1.uid).one()
                d={'id':book.id,'bookname':book.b_name,'section_id':book.section_id,'authorname':book.author_name,'coverphoto':book.b_photo,'username':u.stored_username,'email':u.stored_email,'type':'assign','doi':ib1.issue_date,'dor':ib1.return_date,'daysleft':(ib1.return_date-datetime.now()).days,'hoursleft':int((ib1.return_date-datetime.now()).seconds)//3600,'uid':ib1.uid}
            else:
                d={'id':book.id,'bookname':book.b_name,'section_id':book.section_id,'authorname':book.author_name,'coverphoto':book.b_photo,'type':'free'}
            input_data.append(d)
        return jsonify({'data':input_data,'msg':'Success'}),201
    if user.role=='user':
        books=Books.query.all()
        input_data=[book.to_dict() for book in books]
        return jsonify({'data':input_data,'msg':'Success'}),201
    return jsonify({"msg":"Fail"}),209

@myapplication.route("/addsection",methods=["POST"])
@jwt_required()
def addsection():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role != 'admin':
        return jsonify({'msg':'You are not authorised'}),403
    sname=request.form.get('Section Name')
    des=request.form.get("Descryp")
    book_ids=list(request.form.get("SelectedOptions").split(','))
    section_exist=Section.query.filter(Section.s_name==sname).first()
    if section_exist:
        return jsonify({'msg':'Section already exist'}),409
    new_section=Section(s_name=sname,description=des)
    
    db.session.add(new_section)
    db.session.commit()
    if len(book_ids)==1:
        return jsonify({'msg':'Section added successfully'}),201
    thissection=Section.query.filter(Section.s_name==sname).first()
    if len(book_ids)>1:
        for i in range(1,len(book_ids)):
            book=Books.query.filter(Books.id==book_ids[i]).first()
            book.section_id=thissection.id
            db.session.commit()
    return jsonify({'msg':'Section added successfully'}),201


@myapplication.route("/editsection",methods=["POST"])
@jwt_required()
def editsection():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role != 'admin':
        return jsonify({'msg':'You are not authorised'}),409
    sid=request.form.get("sid")
    sname=request.form.get('s_name')
    des=request.form.get("descryp")
    book_ids=list(request.form.get("SelectedOptions").split(','))    
    if not sid:
        return jsonify({'msg':'Some error occured'}),403
    new_section=Section.query.filter(Section.id==sid).one()
    old_books=Books.query.filter(Books.section_id==sid).all()
    for b in old_books:
        if b.id not in book_ids:
            b.section_id=None
    try:
        new_section.s_name=sname
        new_section.description=des
        db.session.commit()
        thissection=Section.query.filter(Section.s_name==sname).first()
        for bid in book_ids:
            book=Books.query.filter(Books.id==bid).first()
            book.section_id=thissection.id
            db.session.commit()
        return jsonify({'msg':'Success'}),201
    except Exception as e:
        db.session.rollback()
        #print(e)
        return jsonify({'msg':'Failed editing the section! Try again.'}),409



@myapplication.route("/requestbook",methods=["POST","GET"])
@jwt_required()
def requestbook():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role == 'admin':
        if request.method=="GET":
            bookrequests=BookIssue.query.filter(BookIssue.book_status==0).all()
            input_data=[]
            for book in bookrequests:
                b=Books.query.filter(Books.id==book.bid).one()
                u=User.query.filter(User.id==book.uid).one()
                delta=book.return_date-book.issue_date
                d={'id':book.id,'bookname':b.b_name,'authorname':b.author_name,'coverphoto':b.b_photo,'username':u.stored_username,'email':u.stored_email,'hrs':int(delta.seconds)//3600,'days':int(delta.days)%7,'weeks':int(delta.days)//7}
                input_data.append(d)
            return jsonify({"msg":"success","input_data":input_data}),201
        if request.method == 'POST':
            reqid=request.form.get('reqid')
            accept=request.form.get('type')
            reqbook=BookIssue.query.filter(BookIssue.id==reqid).one()
            try:
                if accept=='1':
                    diff=reqbook.return_date-reqbook.issue_date
                    reqbook.issue_date=datetime.now()
                    reqbook.return_date=datetime.now()+diff
                    reqbook.book_status=1
                else:
                    book=Books.query.filter(Books.id==reqbook.bid).one()
                    requser=User.query.filter(User.id==reqbook.uid).one()
                    book.avail_status=1
                    requser.count-=1
                    db.session.delete(reqbook)
                db.session.commit()
                return jsonify({"msg":"Success"}),201
            except Exception as e:
                db.session.rollback()
                return jsonify({'msg':f'Some error occured {str(e)}'}),409
    if user.role != 'user':
        return jsonify({'msg':'You are not authorised'}),409
    if user.count>=5:
        return jsonify({"msg":"You can request and have maximum of 5 books"}),201
    data=request.get_json()
    bookid=data.get('bookid')
    hrs=data.get('hrs')
    days=data.get('days')+data.get('weeks')*7
    #print(days)
    book=Books.query.filter(Books.id==bookid).one()
    if not book:
        return jsonify({"msg": "Something went wrong on our side(book doesnt exist)"}),407
    if book.avail_status == 0:
        return jsonify({"msg":"Book is not available currently"})
    bookissue=BookIssue(uid=user.id,bid=book.id,issue_date=datetime.now(),return_date=datetime.now()+timedelta(hours=hrs,days=days),book_status=0)
    try:
        db.session.add(bookissue)
        book.avail_status=0
        user.count+=1
        db.session.commit()
        return jsonify({'msg':'Success'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg':f'Some error occured {str(e)}'}),409

@myapplication.route("/getsections",methods=["POST","GET"])
@jwt_required()
def getsections():
    cur_user=get_jwt_identity()
    if not cur_user:
        return jsonify({"msg":"Fail"}),409
    section=Section.query.all()
    sec=[sect.to_dict() for sect in section]
    return jsonify({"msg":"Success","input_section":sec}),201

@myapplication.route("/curbooks", methods=["GET"])
@jwt_required()
def curbooks():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role != 'user' or not cur_user:
        return jsonify({"msg":"Fail"}),409
    current_books=BookIssue.query.filter(BookIssue.uid == user.id ,BookIssue.book_status == 1).all()
    past_books=BookIssue.query.filter(BookIssue.uid == user.id ,BookIssue.book_status == 2).all()
    pst_books=[book.to_dict() for book in past_books]
    cur_books=[book.to_dict() for book in current_books]
    return jsonify({"msg":"Success","input_curbooks":cur_books,"input_pastbooks":pst_books}),201

@myapplication.route("/returnbook",methods=["POST"])
@jwt_required()
def returnbook():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    data=request.get_json()
    if not cur_user:
        return jsonify({"msg":"Please login again"}),409
    if user.role == 'admin':
        bid=data.get("bookid")
        uid=data.get("userid")
        revokeuserdel=User.query.filter(User.id==uid).one_or_none()
        revokebook=BookIssue.query.filter(BookIssue.bid==bid ,BookIssue.uid==uid ,BookIssue.book_status==1).one_or_none()
        revokebookdels=Books.query.filter(Books.id==bid).one_or_none()
        if not revokebook or not revokebookdels or not revokeuserdel:
            return jsonify({"msg":"Fail"}),409
        revokebookdels.avail_status=1
        revokebook.return_date=datetime.now()
        revokebook.book_status=2
        revokeuserdel.count-=1
        try:
            db.session.commit()
            return jsonify({'msg':"Success"}),201
        except Exception as e:
            db.session.rollback()
            return jsonify({"msg":e}),409
    if user.role == 'user':
        rid=data.get("bookid")
        bookissued=BookIssue.query.filter(BookIssue.bid==rid ,BookIssue.uid==user.id ,BookIssue.book_status==1).one()
        bookdels=Books.query.filter(Books.id==rid).one()
        if not bookissued or not bookdels:
            return jsonify({"msg":"Fail"}),409
        bookdels.avail_status=1
        bookissued.return_date=datetime.now()
        bookissued.book_status=2
        user.count-=1
        try:
            db.session.commit()
            return jsonify({'msg':"Success",'rid':rid}),201
        except Exception as e:
            db.session.rollback()
            return jsonify({"msg":"Failed to return, try again later"}),409
    
@myapplication.route("/ratebook",methods=['POST'])
@jwt_required()
def rate():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    data=request.get_json()
    book_id=data.get("bookid")
    rate=data.get("ratevalue")
    if user.role !='user' or not cur_user or not book_id or not rate:
        return jsonify({"msg":"Failed to rate, try again later1"}),409
    rate_exist=Rating.query.filter(Rating.bid==book_id,Rating.uid==user.id).first()
    if not rate_exist:
        new_rate=Rating(uid=user.id,bid=book_id,value=rate)
        try:
            db.session.add(new_rate)
            db.session.commit()
            stored_rates=[rateing.to_dict() for rateing in user.stored_rating]
            return jsonify({'msg':"Success",'stored_rating':stored_rates,'rate':rate}),201
        except Exception as e:
            db.session.rollback()
            return jsonify({"msg":"Failed to rate, try again later2"}),409
    else:
        try:
            rate_exist.value=rate
            db.session.commit()
            stored_rates=[rateing.to_dict() for rateing in user.stored_rating]
            return jsonify({'msg':"Success",'stored_rating':stored_rates,'rate':rate}),201
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({"msg":"Failed to rate, try again later3"}),409

@myapplication.route('/logout',methods=['POST'])
@jwt_required()
def logout():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if not cur_user or not user:
        return jsonify({"msg":"Token expired"}),403#
    user.last_visited=datetime.now(timezone("Asia/Kolkata"))
    db.session.commit()
    response=jsonify({"msg":"Logout Successful"})
    unset_jwt_cookies(response)
    return jsonify({"msg":"Logout Successful"}), 201


@myapplication.route("/removebook",methods=["POST"])
@jwt_required()
def removebook():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role !='admin' or not cur_user:
        return jsonify({"msg":"You are not authorised to perform this"}),409
    bid=request.form.get("bid")
    book=Books.query.filter(Books.id==bid).one()
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"msg":"Success"}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg':f'Some error occured {str(e)}'}), 409
    

@myapplication.route("/removesection",methods=["POST"])
@jwt_required()
def removesection():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role !='admin' or not cur_user:
        return jsonify({"msg":"You are not authorised to perform this"}),409
    sid=request.form.get("sid")
    sec=Section.query.filter(Section.id==sid).one()
    try:
        db.session.delete(sec)
        db.session.commit()
        return jsonify({"msg":"Success"}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg':f'Some error occured {str(e)}'}), 409

@myapplication.route("/editbook",methods=["post"])
@jwt_required()
def editbook():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role != 'admin':
        return jsonify({'msg':'Access denied. Only librarian can add books'}),403
    bookname=request.form.get("bookname")
    authorname=request.form.get("authorname")
    bid=request.form.get("bid")
    book=Books.query.filter(Books.id==bid).one()
    if not book:
        return jsonify({'msg':'something went wrong'}),409
    file1=request.files['file1']
    file2=request.files['file2']
    if not file1 or not file2 or not bookname or not authorname:
        return jsonify({"msg":"Give all fields mentioned"}),409
    if not allow_pdffile(file1.filename):
        return jsonify({"msg":"Upload books of Pdf format only"}),409
    if not allow_imagefile(file2.filename):
        return jsonify({"msg":"Upload coverphoto of jpg/png format only"}),409
    book_filename="book_"+secure_filename(bookname)+file1.filename
    coverphoto_filename="cv_"+secure_filename(bookname)+file2.filename
    old_photo=book.b_photo
    old_content=book.book_content
    input_book="books/"+book_filename
    input_cover="coverphotos/"+coverphoto_filename
    try:
        book.b_name=bookname
        book.author_name=authorname
        book.b_photo=input_cover
        book.book_content=input_book
        db.session.commit()
        os.remove(os.path.join(myapplication.root_path,'../../frontend/public/',old_photo))
        os.remove(os.path.join(myapplication.root_path,'../../frontend/public/',old_content))
        file1.save(os.path.join(myapplication.root_path,'../../frontend/public/books/',book_filename))
        file2.save(os.path.join(myapplication.root_path,'../../frontend/public/coverphotos/',coverphoto_filename))
        return jsonify({'msg':'Success'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg':f'Some error occured {str(e)}'}),409
    
@myapplication.route("/changepassword",methods=["post"])
@jwt_required()
def changepass():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    data=request.get_json()
    oldpass=data.get('oldPass')
    newpass=data.get('newPass')
    if not check_password_hash(user.stored_password,oldpass):
        return jsonify({'msg':'Password incorrect'}),203
    user.stored_password=generate_password_hash(newpass)
    db.session.commit()
    x=passwordchange_reply(user.id)
    return jsonify({'msg':'Password change Successful'}),201

@myapplication.route("/getuser",methods=["get"])
@jwt_required()
def userdels():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if not user:
        return jsonify({'msg':'User not found'}),203
    return jsonify({'msg':'Success','name':user.stored_name,'username':user.stored_username,'email':user.stored_email,'bcount':user.count}),201

@myapplication.route("/downloaddata",methods=["POST"])
@jwt_required()
def getdata():
    cur_user=get_jwt_identity()
    user=User.query.get(cur_user['id'])
    if user.role =='admin':
        data=request.get_json()
        start_date=datetime.strptime(data.get("start_date"), "%Y-%m-%d")
        end_date=datetime.strptime(data.get("end_date"), "%Y-%m-%d")+timedelta(days=1)
        book_issues = BookIssue.query.filter(and_(BookIssue.issue_date>=start_date,BookIssue.issue_date<=end_date)).all()
        book_res="BookName,AuthorName,UserName,email,issue date,return date\n"
        for book_issue in book_issues:
            user=User.query.filter(User.id==book_issue.uid).one()
            book=Books.query.filter(Books.id==book_issue.bid).one()
            book_res+=f"{book.b_name},{book.author_name},{user.stored_name},{user.stored_email},{book_issue.issue_date.strftime('%d-%m-%Y %H:%M:%S')},{book_issue.return_date.strftime('%d-%m-%Y %H:%M:%S')}\n"
            

        response = Response(book_res, content_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=users.csv"
    
        return response
    return jsonify({'msg':'Access denied. Only librarian can add books'}),403