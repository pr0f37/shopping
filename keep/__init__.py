import gkeepapi


def export_to_keep(recipes, email, password):
    try:
        keep = gkeepapi.Keep()
        keep.login(email, password)
        my_note = keep.createList('ByShoppingPortal')
        for recipe, ingredients in recipes:
            list_item = my_note.add(recipe, checked=False)
            for ingredient in ingredients:
                list_item.add(ingredient, checked=False)
        my_note.pinned = True
        keep.sync()
        return 'Your recipes have been exported'
    except Exception as ex:
        return ex.__str__()
