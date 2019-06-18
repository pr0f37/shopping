import gkeepapi


def ings_to_exp(ingredients):
    for ingredient in ingredients:
        if ingredient.amount != '':
            yield(f'{ingredient.name} - {ingredient.amount}')
        else:
            yield(ingredient.name)


def export_to_keep(recipes, email, password):
    try:
        recipes_exp = ((recipe.title, ings_to_exp(recipe.ingredients)) for recipe in recipes)
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
