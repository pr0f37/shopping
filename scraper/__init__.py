from requests_html import HTMLSession
# from planner import db
# from planner.models import Ingredient, Recipe


def lidl(url):
    session = HTMLSession()
    # r = session.get('https://kuchnialidla.pl/makaron-z-kurczakiem-i-pesto-z-rukoli')
    r = session.get(url)
    ingredients = r.html.find('div.skladniki', first=True).find('li')
    ings = []
    for ingredient in ingredients:
        ings.append(tuple(ingredient.text.split(' – ')))
        # print(ing)
    tytul = r.html.find('div.lead', first=True).find('h1', first=True)
    # print(tytul.text)
    czas = r.html.find('li.meta_time', first=True).find('strong', first=True)
    # print(czas.text)
    poziom = r.html.find('li.meta_level', first=True).find('em', first=True)
    # print(poziom)
    liczba_porcji = r.html.find('li.meta_size', first=True)
    # print(liczba_porcji)
    przepis = r.html.find('div.article#opis', first=True)
    # print(przepis.text)
    # rec = Recipe(name)
    return {'name': tytul.text, 'time': czas.text, 'text': przepis.text, 'ingredients': ings}

    # rec = lidl('url do przepisu lidla')
    # recipe = Recipe(name=rec.name, time=rec.time, text=rec.recipe, author=current_user)
    # ingredients = [Ingredient(name=x, amount=y[0] if y else '') for x, *y in rec['ingredients']]
    # recipe.ingredients = ingredients
    # db.session.add(recipe)
    # db.session.commit()
