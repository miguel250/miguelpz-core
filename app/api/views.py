from flask import Blueprint, Response, jsonify, request, session
from app.core.models import User

main = Blueprint('api', __name__)

@main.route('/me/<username_id>')
def index(username_id):
    user = User.objects.get_or_404(id=username_id)
    message = {
        'status': 200,
         'info': {
            'job': user.job,
            'name': user.name,
            'city': user.city,
            'pesonal_website': user.personal_web
        },
        'social' : {
            'github': user.github,
            'twitter': user.twitter,
            'linkedin': user.linkedin,
            'facebook': user.facebook,
            'googleplus': user.googleplus,
            'foursquare': user.foursquare,
            'personal_web': user.personal_web,
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