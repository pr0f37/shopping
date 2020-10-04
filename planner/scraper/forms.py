from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL


class ScraperForm(FlaskForm):
    recipe_url = StringField("Recipe url", validators=[DataRequired(), URL()])
    submit = SubmitField("Scrape")
