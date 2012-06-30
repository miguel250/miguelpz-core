from app.core.models import User
from flask.ext.wtf import Form, TextField, TextAreaField, PasswordField, \
                          SubmitField, ValidationError, validators, Required, \
                          Email 

class UserSettingsForm(Form):
    username =      TextField('Username', [Required(),validators.Length(min=4, max=25)])
    email =         TextField('Email', [Required(), Email()])
    job =           TextField('Job')
    city =          TextField('City')
    name =          TextField('Name',)
    github =        TextField('Github')
    twitter =       TextField('Twitter')
    linkedin =      TextField('Linkedin')
    facebook =      TextField('Facebook')
    googleplus =    TextField('Google+')
    foursquare =    TextField('Foursquare')
    personal_web  = TextField('Personal Website')
    submit = SubmitField('Save')