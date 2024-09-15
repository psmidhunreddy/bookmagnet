from flask import jsonify, make_response,Blueprint,request
from ..models import Books,db,Section,User
from .validation import NotFoundError, BusineesValidationError, BadRequest
from flask_restful import Resource, fields, marshal_with, reqparse
import werkzeug,os
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies

myapplication=Blueprint('apps',__name__)
book_fields={
    "id": fields.Integer,
    "b_name": fields.String,
    "author_name": fields.String,
    "avail_status": fields.Integer,
    "section_id":fields.Integer,
    "b_photo": fields.String,
    "book_content":fields.String
}

class BookAPI(Resource):
    @marshal_with(book_fields)
    def get(self, book_id=None):
        if book_id == None  :
            books= Books.query.all()
            if len(books)==0:
                raise NotFoundError(error_message="No Books present")
            else:
                return books
        else:
            books = Books.query.filter(Books.id==book_id).first()
            if not books:
                raise NotFoundError(error_message="Book not found")
            else:
                return books
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if not user or not user.role=='admin':
            return jsonify({'message': 'Access denied. You must be an admin to add a Book.'}), 403
        #print("Content-Type:", request.content_type)
        book_parser=reqparse.RequestParser()
        book_parser.add_argument('input_book_name', required=True, help="Book name is required!",location="form")
        book_parser.add_argument('input_author_name', required=True, help="Author name is required!",location="form")
        book_parser.add_argument('input_section_id',location="form")
        book_parser.add_argument('input_book_photo', type=werkzeug.datastructures.FileStorage, location='files', required=True, help="File is required!")
        book_parser.add_argument('input_book_content', type=werkzeug.datastructures.FileStorage, location='files', required=True, help="File is required!")
        args = book_parser.parse_args()
        input_book_name=args.get("input_book_name", None)
        input_author_name=args.get("input_author_name", None)
        input_section_id=args.get("input_section_id",None)
        book_photo_file=args['input_book_photo']
        book_content_file=args['input_book_content']
        
        if Books.query.filter(Books.b_name==input_book_name).first():
            raise BusineesValidationError(error_message="Book with "+ input_book_name + " name exist. Give some other name")
        if input_section_id and not Section.query.filter(Section.id==input_section_id).first():
            raise BadRequest(error_message="Section with id " + str(input_section_id) + " doesn't exist")
        input_book_photo="cv_"+secure_filename(input_book_name)+book_photo_file.filename
        input_book_content="book_"+secure_filename(input_book_name)+book_content_file.filename
        book_photo_file.save(os.path.join(myapplication.root_path,'../../../frontend/public/coverphotos/',input_book_photo))
        book_content_file.save(os.path.join(myapplication.root_path,'../../../frontend/public/books/',input_book_content))
        input_book="books/"+input_book_content
        input_cover="coverphotos/"+input_book_photo
        new_book=Books(b_name=input_book_name,author_name=input_author_name,b_photo=input_cover,avail_status=1,book_content=input_book,section_id=input_section_id)
        db.session.add(new_book)
        db.session.commit()
        return new_book.to_dict(),201 
    @jwt_required()
    def delete(self,book_id=None):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if not user or not user.role=='admin':
            return jsonify({'message': 'Access denied. You must be an admin to delete a Book.'}), 403
        if book_id!= None :
            books = Books.query.filter(Books.id==book_id).first()
            if not books:
                raise BadRequest(error_message="Book with id " + str(book_id) + " doesn't exist")
            else:
                db.session.delete(books)
                db.session.commit()
            return make_response(jsonify({"message":"Book with id " + str(book_id) + " successfully deleted"}),200)
        else:
            raise BadRequest(error_message="Please give book id")
    @marshal_with(book_fields)
    @jwt_required()
    def put(self,book_id=None):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if not user or not user.role=='admin':
            return jsonify({'message': 'Access denied. You must be an admin to edit a Book.'}), 403
        book_parser=reqparse.RequestParser()
        book_parser.add_argument('input_book_name', required=True, help="Book name is required!")
        book_parser.add_argument('input_author_name', required=True, help="Author name is required!")
        book_parser.add_argument('input_section_id')
        book=Books.query.filter(Books.id==book_id).first()
        if not book:
            raise BadRequest(error_message="There is no book with id " + str(book_id))
        else:
            args = book_parser.parse_args()
            input_book_name=args.get("input_book_name", None)
            input_author_name=args.get("input_author_name", None)
            input_section_id=args.get("input_section_id", None) #
            if input_section_id and not Section.query.filter(Section.id==input_section_id).first():
                raise BadRequest(error_message="Section with id " + str(input_section_id) + " doesn't exist")
            if Books.query.filter(Books.b_name==input_book_name).first():
                raise BusineesValidationError(error_message="Book with "+ input_book_name + " name already exist. Give some other name")
            book.b_name=input_book_name
            book.author_name=input_author_name
            book.section_id=input_section_id
            db.session.commit()
            return book 