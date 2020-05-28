from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from datetime import date
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    # for administrator add in booleon logic later

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired()])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # when you add any methods that match the pattern validate_<>, WTForms invokes in addition to stock
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    # def validate_email(self, email):
    #     user = User.query.filter_by(email = email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')


class LeaveRequestForm(FlaskForm):
    startdate = DateField('Start date', format= '%Y-%m-%d')
    enddate = DateField('End date', format= '%Y-%m-%d')
    note = TextAreaField('Note')
    halfdaybegin = BooleanField('Take a half day at the beginning of leave')
    halfdayend = BooleanField('Take a half day at the end of leave')
    submit = SubmitField('Submit Request')

    # def __init__(self,*args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.startdate.data:
    #         self.startdate.data =date.today() 
    #     if not self.enddate.data:
    #         self.enddate.data = date.today() 

    # def validate_startdate(self, startdate):
    #     if self.startdate.data < date.today():
    #         raise ValidationError('Please enter a valid starting date')
    # def validate_enddate(self, enddate):
    #     if self.enddate.data < date.today():
    #         raise ValidationError('Please enter a valid ending date')
    # def validate_dates(self):
    #     if self.enddate.data < self.startdate.data:
    #         raise ValidationError("Start date is later than enddate")

class PublicHolidaysForm(FlaskForm):
    name = StringField('Holiday Name', validators= [DataRequired()])
    date = DateField('Date', format = '%Y-%m-%d')
    submit = SubmitField('Submit Holiday')


