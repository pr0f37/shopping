import gkeepapi


def ingredients_to_export(ingredients):
    for ingredient in ingredients:
        if ingredient.amount != '':
            yield(f'{ingredient.name} - {ingredient.amount}')
        else:
            yield(ingredient.name)


def recipes_to_export(recipes):
    for recipe in recipes:
        yield(recipe.title, ingredients_to_export(recipe.ingredients))


def export_to_keep(recipes, email, password):
    try:
        recipes_exp = recipes_to_export(recipes)
        keep = gkeepapi.Keep()
        keep.login(email, password)
        my_note = keep.createList('ByShoppingPortal')
        for recipe, ingredients in recipes_exp:
            list_item = my_note.add(recipe, checked=False)
            for ingredient in ingredients:
                list_item.add(ingredient, checked=False)
        my_note.pinned = True
        keep.sync()
        return 'Your recipes have been exported'
    except Exception as ex:
        return ex.__str__()
