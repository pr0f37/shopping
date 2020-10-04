from flask import Blueprint, render_template, request

from planner.models import Recipe

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    recipe_list = Recipe.query.order_by(Recipe.date_posted.desc()).paginate(
        page=page, per_page=5
    )
    return render_template("home.html", recipe_list=recipe_list, title="Home")


@main.route("/about")
def about():
    return render_template("about.html", title="About")
