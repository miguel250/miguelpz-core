import json
from app import config
from flask import Blueprint, Response, jsonify, request, session
from app.core.models import User
from flaskext.mail import Message

main = Blueprint('api', __name__)

@main.route('/me/contact/<username>',methods=['POST', 'OPTIONS'])
def contact(username):
    user = User.objects.get_or_404(username=username)
    message = {'status': 200}

    if request.method == 'POST':
        data = request.data
        email  = json.loads(data)
        contact_name = email['name']
        contact_email = email['email']
        subject = email['subject']
        body =  email['body']


        message = {
            'name': {'error':  0 if len(contact_name) else 1, 'value': contact_name},
            'email': {'error': 0 if len(contact_email) else 1, 'value': contact_email},
            'subject': {'error': 0 if len(subject) else 1, 'value': subject},
            'body': {'error': 0 if len(body) else 1, 'value': body},
        }

        if len(contact_name) == 0 or len(contact_email) == 0 or len(subject) == 0 or len(body) == 0:
            message['status'] = 422
            resp = jsonify(message)
            resp.status_code = 200
            return resp

        msg = Message(subject, reply_to="%s <%s>"%(contact_name, contact_email))
        msg.add_recipient(user.email)
        msg.body = body
        config.mail.send(msg)


        message = {'status': 200, 'message': 'Thanks for your message %s! I will get back to you as soon as posible'%contact_name}
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@main.route('/me/<username>')
def me(username):
    user = User.objects.get_or_404(username=username)
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