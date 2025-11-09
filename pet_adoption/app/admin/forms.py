from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Optional, Length
from flask_wtf.file import FileField, FileAllowed


class PetForm(FlaskForm):
    """Form for creating and editing pet records in the admin UI."""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    availability = SelectField(
        'Availability',
        choices=[('available', 'Available'), ('adopted', 'Adopted'), ('foster', 'Foster')],
        validators=[DataRequired()]
    )
    type = StringField('Type', validators=[Optional(), Length(max=50)])
    breed = StringField('Breed', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=2000)])
    disposition = TextAreaField('Disposition', validators=[Optional()])
    news_item = BooleanField('Feature as news item', default=False)
    public_image = FileField('Public Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
