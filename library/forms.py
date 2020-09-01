from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, PasswordField, SubmitField, BooleanField,RadioField,IntegerField,FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegisterationForm(FlaskForm):
    first_name =        StringField('First Name',validators=[DataRequired(),Length(min=3,max=20)])
    last_name =         StringField('Last Name', validators=[DataRequired(),Length(min=3,max=20)])
    b_day =             StringField('Birthday',validators=[DataRequired(),Length(min=10,max=10)])
    address =           StringField('Address', validators=[DataRequired(),Length(min=3,max=50)])
    town =              StringField('Town', validators=[DataRequired(),Length(min=3,max=20)])
    postal_code =       IntegerField('Postal Code', validators=[DataRequired()])
    username =          StringField('Username', validators=[DataRequired(),Length(min=3,max=20)])
    password =          PasswordField('Password',validators=[DataRequired()])
    confirm_password =  PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit =            SubmitField('Sign Up')
    
    
class EmpRegisterationForm(FlaskForm):
    first_name =        StringField('First Name',validators=[DataRequired(),Length(min=3,max=20)])
    last_name =         StringField('Last Name', validators=[DataRequired(),Length(min=3,max=20)])
    salary =            FloatField('Salary',validators=[DataRequired()])
    perm_temp =         RadioField('Perm or Temp',validators=[DataRequired()],choices=[('perm', 'Permanent'),('temp','Temporary')],)              
    perm_date =         DateField('Perm Date')
    temp_number =       IntegerField('Temp Number')
    username =          StringField('Username', validators=[DataRequired(),Length(min=3,max=20)])
    password =          PasswordField('Password',validators=[DataRequired()])
    confirm_password =  PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit =            SubmitField('Add Emploee')

class BookRegisterationForm(FlaskForm):
    title =             StringField('Title',validators=[DataRequired(),Length(min=3,max=20)])
    year =              IntegerField('Year')
    page_cnt =          IntegerField('Page Count')
    publisher  =        StringField('Name',validators=[DataRequired(),Length(min=3,max=20)])
    number_of_copies =  IntegerField('Number of copies')
    publishers =        SelectField(u'Group', choices=[],validators=[DataRequired()])
    submit =            SubmitField('Add Book')

class PublisherRegisterationForm(FlaskForm):
    name =              StringField('Name',validators=[DataRequired(),Length(min=3,max=20)])
    year =              IntegerField('Year')
    submit =            SubmitField('Add Publisher')
    
class LoginForm(FlaskForm):
    username =          StringField('Username', validators=[DataRequired(),Length(min=4,max=20)])
    password =          PasswordField('Password',validators=[DataRequired()])
    submit =            SubmitField('login')

class Member_form(FlaskForm):
    members =           SelectField(u'Group', choices=[],validators=[DataRequired()])
    remove_member =     SubmitField('Remove')
    update_member =     SubmitField('Update')
    send_reminder =     SubmitField('Send Reminder')

class Emp_form(FlaskForm):
    emps =              SelectField(u'Group', choices=[])
    remove_emp =        SubmitField('Remove')
    add_emp =           SubmitField('Add')
    update_emp  =       SubmitField('Update')

class Book_form(FlaskForm):
    books =             SelectField(u'Group', choices=[])
    borrowed_books =    SelectField(u'Group', choices=[]) 
    remove_book =       SubmitField('Remove')
    add_book =          SubmitField('Add')
    update_book =       SubmitField('Update')
    borrow_book =       SubmitField('Borrow')
    return_book =       SubmitField('Return')

class Publisher_form(FlaskForm):
    publishers =        SelectField(u'Group', choices=[])
    name =              StringField('Name',validators=[DataRequired()])
    year =              IntegerField('Year',validators=[DataRequired()])
    remove_publisher =  SubmitField('Remove')
    add_publisher =     SubmitField('Add')
    update_publisher  = SubmitField('Update')
    
