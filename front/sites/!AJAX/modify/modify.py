import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    data = kwg['data']
    mid =               bottle.request.forms.getunicode('mid', None)
    title =             bottle.request.forms.getunicode('title', '')
    age =               bottle.request.forms.getunicode('age', 0)
    director =          bottle.request.forms.getunicode('director', '')
    production =        bottle.request.forms.getunicode('production', 0)
    stock =             bottle.request.forms.getunicode('stock', 0)
    description =       bottle.request.forms.getunicode('description', '')
    #categories =       bottle.request.forms.getunicode('categories', '')

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