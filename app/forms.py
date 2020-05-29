from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, PublicHolidays
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
    startdate = DateField('Start date', format= '%Y-%m-%d', validators=[DataRequired()])
    enddate = DateField('End date', format= '%Y-%m-%d',  validators=[DataRequired()])
    note = TextAreaField('Note')
    halfdaybegin = BooleanField('Take a half day at the beginning of leave')
    halfdayend = BooleanField('Take a half day at the end of leave')
    submit = SubmitField('Submit Request')

   
    def validate(self):
        if not super().validate():
            return False
        result = True
        if self.enddate.data < self.startdate.data:
            self.enddate.errors.append('End date must not be earlier than start date')
            result = False
        return result

    def validate_startdate(self, startdate):
        if startdate.data < date.today():
            raise ValidationError('Choose a valid start date')

        publicholiday = PublicHolidays.query.filter_by(date = startdate.data).first()
        if publicholiday is not None:
            # start date is a public holiday
            raise ValidationError('Start date is a public holiday, choose another startdate')
    def validate_enddate(self, enddate):
        if enddate.data < date.today():
            raise ValidationError('Choose a valid end date')
        publicholiday = PublicHolidays.query.filter_by(date = enddate.data).first()
        if publicholiday is not None:
            # start date is a public holiday
            raise ValidationError('End date is a public holiday, choose another startdate')

class PublicHolidaysForm(FlaskForm):
    name = StringField('Holiday Name', validators= [DataRequired()])
    date = DateField('Date', format = '%Y-%m-%d')
    submit = SubmitField('Submit Holiday')

    def validate_name(self, name):
        publicholiday = PublicHolidays.query.filter_by(name = name.data).first()
        if publicholiday is not None:
            # cannot have two holidays of the same name
            raise ValidationError('Public holiday has already been added please enter another Holiday')
