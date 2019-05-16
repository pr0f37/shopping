import gkeepapi

keep = gkeepapi.Keep()
keep.login('user', 'passwd')

# retrieve note/list
# my_note = keep.get('noteId')
# or create new note
# my_note = keep.createNote('Note Title')
# or create new list
my_note = keep.createList('List Title')
# add new item to list
my_note_item = my_note.add(text='Item text',checked=False)

print(my_note.items)

# creating subitems
my_note_subitem = my_note_item.add(text='SubItem text',checked=False)

keep.sync()
