from requests_html import HTMLSession


def scrape(url):
    if 'lidl' in url:
        return lidl(url)
    return None


def lidl(url):
    try:
        session = HTMLSession()
        r = session.get(url)
        ingredients_html = r.html.find('div.skladniki', first=True).find('li')
        ingredients = []
        for ingredient in ingredients_html:
            ingredients.append(tuple(ingredient.text.split(' – ')))
        name = r.html.find('div.lead', first=True).find('h1', first=True)
        time = r.html.find('li.meta_time', first=True).find('strong', first=True)
        # level = r.html.find('li.meta_level', first=True).find('em', first=True)
        # porition_number = r.html.find('li.meta_size', first=True)
        recipe_text = r.html.find('div.article#opis', first=True)
        return {'name': name.text,
                'time': time.text,
                'text': recipe_text.text,
                'ingredients': ingredients}
    except Exception as ex:
        return None
