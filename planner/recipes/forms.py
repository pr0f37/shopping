from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class RecipeForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    ingredient_name = StringField("Ingredient[]")
    ingredient_amount = StringField("Amount[]")
    submit = SubmitField("Post")
