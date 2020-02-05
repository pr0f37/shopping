from flask import Blueprint, render_template, request, jsonify
from pdb import set_trace as bp
from planner.models import Recipe

main_bp = Blueprint('main_bp', __name__)


@main_bp.route("/")
@main_bp.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    recipe_list = Recipe.query.order_by(Recipe.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', recipe_list=recipe_list, title='Home')


@main_bp.route("/about")
def about():
    return render_template('about.html', title='About')


@main_bp.route("/test")
def say_hello():
    recipe_list = [recipe.title for recipe in Recipe.query.all()]
    return jsonify(recipe_list), 200
