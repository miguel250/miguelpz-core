from flask import Blueprint, Response, jsonify, request, session
from models import User

main = Blueprint('api', __name__)

@main.route('/me/')
def index():
    message = {
        'status': 200,
         'info': {
            'job': User.job,
            'name': User.name,
            'city': User.city,
            'pesonal_website': User.personal_web
        },
        'social' : {
            'github': User.github,
            'twitter': User.twitter,
            'linkedin': User.linkedin,
            'facebook': User.facebook,
            'googleplus': User.googleplus,
            'foursquare': User.foursquare,
            'personal_web': User.personal_web,
        },
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@main.errorhandler(404)
def not_found(error):
    response = jsonify({
        'code': 404, 
        'message': 'Not Found'
        })
    response.status_code = 404
    return response

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    """Catch all requests are return not found error"""
    return not_found(path)