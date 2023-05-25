import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    data = kwg['data']

    succ = False
    title = ''

    mid = bottle.request.forms.get('mid',None)
    if mid and mid.isdecimal():
        q = sql.movie_finder()
        if q.isUsefull():
            title = q.getList()[1]
            q = sql.delete_movie(int(mid))
            if not q.isError():
                succ = True
    
    return function(success = succ, movie = title)