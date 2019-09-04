from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length
from wtforms import DateField

# templates for user input fields - these variables will be used to call the APIs and web scrape

class SimForm(FlaskForm):

    location = StringField('Address',
                        validators=[DataRequired(), Length(min=5, max=30)],
                        render_kw={'placeholder': '55555 test st, Northpole, 00001'})
    date = DateField('Start Date', format = '%m/%d/%Y', description = 'Time',
                        render_kw={'placeholder': '06/20/2015 for June 20, 2015'})
    time_span = RadioField('Time Span', 
                        choices=[('1','1 day'),('7','7 days'), ('30', '30 days')], 
                        default= '1 day', validators=[DataRequired()]) # would like to set 1 as default
    submit = SubmitField('Run Simulation')

    # def validate_form(self, zipcode, date):
    # 	if zipcode.data != int:
    # 		raise ValidationError('Please use a valid zipcode')
    	# if date.data > datetime.datetime.now():
    	# 	raise ValidationError('')

class StaticForm(FlaskForm):
# static info will also use latitude to calculate the tilt angle when displaying info
    bill = StringField('What is your average monthly energy bill?', dsecription = 'dollar ammount',
        validators= #should be a dollar ammount float/integer

    peak_hours = RadioField('Does your utility provider charge for peak hours',
        choices=[('Yes', 1, "No", 0)], validators=[DataRequired()])

    time_zone = StringField('What is your time zone'), dsecription='GMT+/-',
        validators=[Length(min=2, max=3)],
        render_kw={'placeholder': '-4 for EST, -6 for MST'}
