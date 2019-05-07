from flask import Flask, render_template, url_for
app = Flask(__name__)
recipe_list = [
    {
        'name': 'Jajecznica',
        'ingredients':[
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
        'ingredients':[
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
                    Dodać passatę, doprawić pieprzem, solą, kminem i odrobiną cukru.
                    Smażyć na wolnym ogniu aż do zgęstnienia passaty.
                    Utworzyć na powieżchni passaty 3 dołki.
                    Wboj po jednym jajku do każdego dołka. 
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
    return render_template('recipes.html', recipe_list=recipe_list, title='Przepisy')

@app.route("/scraper")
def scraper():
    return render_template('scraper.html', title='Scraper')

if __name__ == "__main__":
    app.run(debug=True)
    