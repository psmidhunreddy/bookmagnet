from flask import jsonify, make_response,Blueprint,request
from ..models import Books,db,Section,User
from .validation import NotFoundError, BusineesValidationError, BadRequest
from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.utils import secure_filename
from datetime import  datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies

class DateFormat(fields.Raw):
    def format(self, value):
        return value.strftime("%d-%m-%Y %H:%M:%S")

section_fields={
    "id": fields.Integer,
    "s_name": fields.String,
    "description": fields.String,
    "doc":DateFormat
}

section_parser=reqparse.RequestParser()
section_parser.add_argument('input_section_name', required=True, help="Section name is required!")
section_parser.add_argument('input_description', required=True, help="Description  is required!")

class SectionAPI(Resource):
    @marshal_with(section_fields)
    def get(self, section_id=None):
        if section_id==None:
            sections= Section.query.all()
            if len(sections)==0:
                raise NotFoundError(error_message="No Books present")
            else:
                return sections
        else:
            section = Section.query.filter(Section.id==section_id).first()
            if not section:
                raise NotFoundError(error_message="Book with "+str(section_id)+" not found")
            else:
                return section
    @jwt_required()
    @marshal_with(section_fields)
    def post(self):
        
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if not user or not user.role=='admin':
            return jsonify({'message': 'Access denied. You must be an admin to add a section.'}), 403
        args = section_parser.parse_args()
        input_section_name=args.get("input_section_name", None)
        input_description=args.get("input_description", None)
        if input_section_name == Section.s_name:
            raise BusineesValidationError(error_message="Section with "+ input_section_name + " name exist. Give some other name")
        new_section=Section(s_name=input_section_name,description=input_description,doc=datetime.now())
        db.session.add(new_section)
        db.session.commit()
        return new_section,201
    @jwt_required()
    @marshal_with(section_fields)
    def put(self,section_id=None):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if not user or not user.role=='admin':
            return jsonify({'message': 'Access denied. You must be an admin to edit a section.'}), 403
        args = section_parser.parse_args()
        input_section_name=args.get("input_section_name", None)
        input_description=args.get("input_description", None)
        section =Section.query.filter(Section.id==section_id).first()
        if not section:
            raise BusineesValidationError(error_message="Section with "+ str(section_id) + " doesnt exist")
        if Section.s_name==input_section_name:
                raise BusineesValidationError(error_message="Section with "+ str(input_section_name) + " name already exist. Give some other name")
        section.s_name=input_section_name
        section.description=input_description
        db.session.commit()
        return section.to_dict(),201
    @jwt_required()
    def delete(self,section_id=None):
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if not user or not user.role=='admin':
            return jsonify({'message': 'Access denied. You must be an admin to delete a section.'}), 403
        if section_id!= None :
            section = Section.query.filter(Section.id==section_id).first()
            if not section:
                raise BadRequest(error_message="Section with id " + str(section_id) + " doesn't exist")
            else:
                db.session.delete(section)
                db.session.commit()
            return make_response(jsonify({"message":"Section with id " + str(section_id) + " successfully deleted"}),200)
        else:
            raise BadRequest(error_message="Please give Section id")
