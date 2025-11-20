from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FileField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed


class PetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired(), Length(min=2, 
                                                                      max=100)])
    type = SelectField('Pet Type', validators=[DataRequired()], choices=[
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('other', 'Other')
    ], validate_choice=True)
    availability = SelectField('Availability', validators=[DataRequired()],
                               choices=[
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
        ('Pending', 'Pending'),
        ('Adopted', 'Adopted')
        ], validate_choice=True)
    breed = StringField('Breed', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=5, max=300)])
    profile_date = DateField('Profile Date', validators=[DataRequired()])

    # SelectMultipleField automatically returns a list which aligns with current DB structure
    disposition = SelectMultipleField('Disposition', validators=[DataRequired()], choices=[
        ('Good with other animals', 'Good with other animals'),
        ('Good with children', 'Good with children'),
        ('Animal must be leashed at all times', 'Animal must be leashed at all times')
    ], validate_choice=True)

    news_item = TextAreaField('News Item', validators=[DataRequired(), 
                                                       Length(min=2, max=300)])
    public_image = FileField('Image File', validators=[
                             FileAllowed(['jpg', 'png', 'jpeg'], 'JPG/PNG/JPEG only')])
    submit = SubmitField('Submit')
