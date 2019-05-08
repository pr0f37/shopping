from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'd3aea4edbd9911a7d1649cb386549c92'

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
