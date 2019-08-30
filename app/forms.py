from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length
from wtforms import DateField

# templates for user input fields - these variables will be used to call the APIs and web scrape

class SimForm(FlaskForm):

    location = StringField('Zipcode',
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