import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from planner import app, db, bcrypt
from planner.forms import RegistrationForm, LoginForm, UpdateAccountForm, RecipeForm
from planner.models import User, Recipe, Ingredient
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/recipes")
@login_required
def recipes():
    recipe_list = Recipe.query.all()
    return render_template('recipes.html', recipe_list=recipe_list, title='Przepisy')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/scraper")
@login_required
def scraper():
    return render_template('scraper.html', title='Scraper')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        ingredients = [Ingredient(name=x, amount=y) for x, y in (zip(request.form.getlist('ingredient_name'), request.form.getlist('ingredient_amount')))]
        recipe = Recipe(title=form.title.data, time=form.time.data, text=form.text.data, author=current_user, ingredients=ingredients)
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been created', 'success')
        return redirect(url_for('recipes '))
    return render_template('create_recipe.html', title='New Recipe', form=form)


@app.route("/recipe/<recipe_id>")
@login_required
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', title=recipe.title, recipe=recipe)


@app.route("/recipe/<recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if current_user != recipe.author:
        abort(403)
    form = RecipeForm()
    form.title.data = recipe.title
    form.time.data = recipe.time
    form.text.data = recipe.text
    # TODO handle ingredients list in the html page
    return render_template('create_recipe.html', title='Update Recipe', form=form, ingredients=recipe.ingredients)