from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from planner import db
from planner.models import Ingredient, Recipe
from . import scrape
from .forms import ScraperForm

scrap = Blueprint('scrap', __name__)


@scrap.route("/scraper", methods=['GET', 'POST'])
@login_required
def scraper():
    form = ScraperForm()
    if form.validate_on_submit():
        recipe_scr = scrape(form.recipe_url.data)
        recipe = Recipe(title=recipe_scr['name'], time=recipe_scr['time'], text=recipe_scr['text'], author=current_user)
        recipe.ingredients = [Ingredient(name=x, amount=y[0] if y else '') for x, *y in recipe_scr['ingredients']]
        db.session.add(recipe)
        db.session.commit()
        flash(f'The recipe has been imported!', 'success') 
        return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
    return render_template('scraper.html', title='Scraper', form=form)
