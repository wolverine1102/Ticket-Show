from werkzeug.exceptions import HTTPException
from flask import make_response, jsonify

class AlreadyExist(HTTPException):
    def __init__(self, status_code, error_message):
        data = {"error_message": error_message }
        self.response = make_response(jsonify(data), status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_message):
        data = {"error_message": error_message }
        self.response = make_response(jsonify(data), status_code)