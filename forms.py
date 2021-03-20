from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Optional, NumberRange, URL


class AddCupcakeForm(FlaskForm):
    """Form for adding cupcakes."""

    flavor = StringField("Flavor", validators=[InputRequired()])
    size = StringField("Size", validators=[InputRequired()])
    image = StringField("Image URL", validators=[URL(), Optional()])
    rating = FloatField("Rating", validators=[InputRequired()])
