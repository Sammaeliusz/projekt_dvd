import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    data = kwg['data']
    mid =               bottle.request.forms.get('mid', None)
    title =             bottle.request.forms.get('title', '')
    age =               bottle.request.forms.get('age', 0)
    director =          bottle.request.forms.get('director', '')
    production =        bottle.request.forms.get('production', 0)
    stock =             bottle.request.forms.get('stock', 0)
    description =       bottle.request.forms.get('description', '')
    #categories =       bottle.request.forms.get('categories', '')

    print(mid, title, age, director, production, stock, description)

    x = lambda n, m : m if len(n) == 0 else int(n)

    age = x(age, 0)
    production = x(production, 0)
    stock = x(stock, 0)

    if sql.movie_exists(int(mid)):
        q = sql.movie_change_add_tags(int(mid), title, [], age, director, production, stock, description)
        if q.isUsefull():
            return function(success = True)
    return function(success = False)