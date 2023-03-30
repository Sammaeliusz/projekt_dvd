import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    movies = sql.movies_recent(8)
    if movies.isUsefull():
        answer = [Struct({
                "name":x[1],
                "categories":x[2],
                "director":x[4],
                "production":x[5],
                "file":f"static/Filmy/{x[1].replace(' ', '-')}.png"
            }) for x in movies.list()]
    else:
        answer = [Struct({
                "name":"",
                "categories":"",
                "director":"",
                "production":0,
                "file":"#"
            })]
    return function(movies = answer)
