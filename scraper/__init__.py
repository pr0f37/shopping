from requests_html import HTMLSession


session = HTMLSession()
r = session.get('https://kuchnialidla.pl/makaron-z-lososiem')
skladniki = r.html.find('.skladniki')
czas = r.html.find('.meta_time', first=True)
poziom = r.html.find('.meta_level', first=True)
liczba_porcji = r.html.find('.meta_size', first=True)
przepis = r.html.find('.recipe_inner', first=True)