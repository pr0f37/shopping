from flask import (Blueprint, render_template, url_for, flash, redirect,
                   request, current_app)
from flask_login import current_user, login_required
from planner import db
from planner.models import Recipe

shopping = Blueprint('shopping', __name__)


@shopping.route("/shopping_list")
@login_required
def shopping_list():
    page = request.args.get('page', 1, type=int)
    recipe_list = Recipe.query.join(Recipe.fans).filter_by(email=current_user.email).paginate(page=page, per_page=5)
    return render_template('shopping_list.html', recipe_list=recipe_list, title='Shopping list')


@shopping.route("/shopping_list/export")
def export():
    recipes_db = current_user.favorite_recipes
    recipes = []
    for recipe in recipes_db:
        ingredients = []
        for ingredient in recipe.ingredients:
            if ingredient.amount != '':
                ingredients.append(f'{ingredient.name} - {ingredient.amount}')
            else:
                ingredients.append(ingredient.name)
        recipes.append((recipe.title, ingredients))
    flash_msg = export_to_keep(recipes, current_user.email, current_app.config['MAIL_PASSWORD'])
    flash(flash_msg, 'success')
    return redirect(url_for('shopping.shopping_list'))


@shopping.route("/shopping_list/<recipe_id>/remove")
@login_required
def shopping_list_remove_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if current_user in recipe.fans:
        recipe.fans.remove(current_user)
        db.session.commit()
    return redirect(url_for('shopping.shopping_list'))