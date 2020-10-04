from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from planner import db
from planner.models import Recipe, Ingredient
from planner.recipes.forms import RecipeForm


recipes = Blueprint("recipes", __name__)


@recipes.route("/recipe/new", methods=["GET", "POST"])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        ingredients = [
            Ingredient(name=x, amount=y)
            for x, y in (
                zip(
                    request.form.getlist("ingredient_name"),
                    request.form.getlist("ingredient_amount"),
                )
            )
        ]
        recipe = Recipe(
            title=form.title.data,
            time=form.time.data,
            text=form.text.data,
            author=current_user,
            ingredients=ingredients,
        )
        db.session.add(recipe)
        db.session.commit()
        flash("Your recipe has been created", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_recipe.html",
        title="New Recipe",
        form=form,
        ingredients=[Ingredient(name="", amount="")],
    )


@recipes.route("/recipe/<recipe_id>")
@login_required
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe.html", title=recipe.title, recipe=recipe)


@recipes.route("/recipe/<recipe_id>/update", methods=["GET", "POST"])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if current_user != recipe.author:
        abort(403)
    form = RecipeForm()
    if form.validate_on_submit():
        ingredients = [
            Ingredient(name=x, amount=y)
            for x, y in (
                zip(
                    request.form.getlist("ingredient_name"),
                    request.form.getlist("ingredient_amount"),
                )
            )
        ]
        recipe.title = form.title.data
        recipe.time = form.time.data
        recipe.text = form.text.data
        for ingredient in recipe.ingredients:
            db.session.delete(ingredient)
        recipe.ingredients = ingredients
        db.session.commit()
        flash("Your recipe has been updated", "success")
        return redirect(url_for("recipes.recipe", recipe_id=recipe.id))
    elif request.method == "GET":
        form.title.data = recipe.title
        form.time.data = recipe.time
        form.text.data = recipe.text
    return render_template(
        "create_recipe.html",
        title="Update Recipe",
        form=form,
        ingredients=recipe.ingredients,
    )


@recipes.route("/recipe/<recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if current_user != recipe.author:
        abort(403)
    for ingredient in recipe.ingredients:
        db.session.delete(ingredient)
    db.session.delete(recipe)
    db.session.commit()
    flash("Your recipe has been deleted", "success")
    return redirect(url_for("main.home"))


@recipes.route("/recipe/<recipe_id>/shoplist")
@login_required
def shop_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if current_user in recipe.fans:
        recipe.fans.remove(current_user)
    else:
        recipe.fans.append(current_user)
    db.session.commit()
    return redirect(url_for("main.home"))
