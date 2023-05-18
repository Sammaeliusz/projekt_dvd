import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    
    movies = sql.movies_recent(99999)
    
    if movies.isUsefull():
        answer = [Struct({
                "id":x[0],
                "name":x[1],
                "categories":x[2],
                "director":x[4],
                "production":x[5],
                "file":f"static/Filmy/{x[1].replace(' ', '-').replace(':', '')}.png"
            }) for x in movies.getList()]

    else:
        answer = []
    return function(movies = answer)
