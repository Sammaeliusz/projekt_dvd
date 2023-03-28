import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    movies = sql.movies_recent(8)
    answer = [Struct({
            "name":x[0][1],
            "categories":x[0][2],
            "director":x[0][4],
            "production":x[0][5],
            "file":f"static/Filmy/{x[0][1].replace(' ', '-')}.png"
        }) for x in movies]
    return function(movies = answer)
