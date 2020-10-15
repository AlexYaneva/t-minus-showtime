from app import table
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_email(self, email):

        # check if a user with this email already exists in the db
        user = table.get_item(Key={"Email": email.data})
        if 'Item' in user:
            raise ValidationError('Please use a different email address.')


class ResetPasswordForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset your password')