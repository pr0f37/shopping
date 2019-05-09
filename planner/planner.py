from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'd3aea4edbd9911a7d1649cb386549c92'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.String(10))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipes', lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

recipe_list = [
    {
        'name': 'Jajecznica',
        'ingredients': [
            {
                'name': 'Jajka',
                'amount': '2',
                'unit': ''
            },
            {
                'name': 'Masło',
                'amount': '10',
                'unit': 'g'
            }
        ],
        'recipe': '''Rozgrzać patelnię.
                    Wrzucić masło na patelnię i poczekać aż się rozpuści.
                    Rozbić jajka i roztrzepać na patelni.
                    Smażyć na wolnym ogniu aż jajka się zetną.
                ''',
        'time': '10 min'
    },
    {
        'name': 'Shakshuka',
        'ingredients': [
            {
                'name': 'Jajka',
                'amount': '3',
                'unit': ''
            },
            {
                'name': 'Olej rzepakowy',
                'amount': '10',
                'unit': 'ml'
            },
            {
                'name': 'Cebula',
                'amount': '1',
                'unit': ''
            },
            {
                'name': 'Passata',
                'amount': '600',
                'unit': 'ml'
            },
            {
                'name': 'Kmin rzymski',
                'amount': '',
                'unit': ''
            },
        ],
        'recipe': '''Rozgrzać patelnię.
                    Na oleju zeszklić cebulę.
                    Dodać passatę, doprawić pieprzem, solą,
                    kminem i odrobiną cukru.
                    Smażyć na wolnym ogniu aż do zgęstnienia passaty.
                    Utworzyć na powieżchni passaty 3 wgłębienia.
                    Wbić po jednym jajku do każdego wgłębienia.
                    Dusić pod przykryciem na wolnym ogniu aż jajka będą ścięte.
                ''',
        'time': '30 min'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/recipes")
def recipes():
    return render_template('recipes.html',
                           recipe_list=recipe_list,
                           title='Przepisy')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/scraper")
def scraper():
    return render_template('scraper.html', title='Scraper')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'passwd':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)
