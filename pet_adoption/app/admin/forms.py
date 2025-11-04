from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Optional, Length


class PetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired(), Length(min=2, max=100)])
    type = SelectField('Pet Type', validators=[DataRequired()], choices=[
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('other', 'other')
    ])
    availability = SelectField('Availability', validators=[DataRequired()], choices=[
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
        ('Pending', 'Pending'),
        ('Adopted', 'Adopted')
        ])
    breed = StringField('Breed', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description', validators=[DataRequired(), Length(min=5, max=300)])
    profile_date = DateField('Profile Date', validators=[DataRequired()])
    
    disposition = SelectField('', validators=[DataRequired()])
    news_item = StringField('News Item', validators=[DataRequired(), Length(min=2, max=300)])
    public_image = 
    submit = SubmitField('Submit')