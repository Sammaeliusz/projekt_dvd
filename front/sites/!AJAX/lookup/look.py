import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    data = kwg['data']
    title =             bottle.request.forms.get('title', '')
    age_min =           bottle.request.forms.get('age_min', 0)
    age_max =           bottle.request.forms.get('age_max', 99)
    director =          bottle.request.forms.get('director', '')
    production_min =    bottle.request.forms.get('production_min', 0)
    production_max =    bottle.request.forms.get('production_max', 9999)
    stock =             bottle.request.forms.get('stock', '0')
    categories =        bottle.request.forms.get('categories', '')

    x = lambda n, m : m if len(n) == 0 else int(n)

    age_min = x(age_min, 0)
    age_max = x(age_max, 99)
    production_min = x(production_min, 0)
    production_max = x(production_max, 9999)
import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    data = kwg['data']
    title =             bottle.request.forms.get('title', '')
    age_min =           bottle.request.forms.get('age_min', 0)
    age_max =           bottle.request.forms.get('age_max', 99)
    director =          bottle.request.forms.get('director', '')
    production_min =    bottle.request.forms.get('production_min', 0)
    production_max =    bottle.request.forms.get('production_max', 9999)
    stock =             bottle.request.forms.get('stock', '0')
    categories =        bottle.request.forms.get('categories', '')

    x = lambda n, m : m if len(n) == 0 else int(n)

    age_min = x(age_min, 0)
    age_max = x(age_max, 99)
    production_min = x(production_min, 0)
    production_max = x(production_max, 9999)

    movies = sql.movies_find_strict(tags=categories.split(','), name = title, age_min = int(age_min), age_max = int(age_max), director = director, production_min = int(production_min), production_max = int(production_max), onstock = stock=='1')
    if movies.isUsefull():
        y = movies.getList()
        if isinstance(y[0], list):
            ans = [Struct({
                "id":x[0],
                "name":x[1],
                "age":x[2],
                "director":x[3],
                "production":x[4],
                "file":f"static/Filmy/{x[1].replace(' ', '-').replace(':','')}.png"
            }) for x in y]
        else:
            ans = [Struct({
                "id":y[0],
                "name":y[1],
                "age":y[2],
                "director":y[3],
                "production":y[4],
                "file":f"static/Filmy/{y[1].replace(' ', '-').replace(':','')}.png"
            })]
        return function(movies = ans)
    return function(movies = [])