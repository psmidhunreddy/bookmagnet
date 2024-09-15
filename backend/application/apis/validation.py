from werkzeug.exceptions import HTTPException
from flask import make_response
from flask import jsonify

class BusineesValidationError(HTTPException):
    def __init__(self, error_message):
        message = {
            "error_message": error_message
            }
        self.response = make_response(jsonify(message), 409)
class NotFoundError(HTTPException):
    def __init__(self, error_message):
        message = {
            "error_message":error_message
        }
        self.response = make_response(jsonify(message), 404)
class BadRequest(HTTPException):
    def __init__(self, error_message):
        message = {
            "error_message":error_message
        }
        self.response = make_response(jsonify(message), 400)