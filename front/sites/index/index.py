import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    data = kwg['data']
    movies = sql.movies_recent(8)
    
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
    movies2 = sql.the_best_movie(8)
    
    if movies2.isUsefull():
        mil = movies2.getList()
        y=[]
        for i in mil:
            y.append(sql.movie_finder(i[0]).getList())
        print(y)
        if isinstance(y[0], list):
            ans2 = [Struct({
                "id":x[0],
                "name":x[1],
                "age":x[2],
                "director":x[3],
                "production":x[4],
                "file":f"static/Filmy/{x[1].replace(' ', '-').replace(':','')}.png"
            }) for x in y]
        else:
            ans2 = [Struct({
                "id":y[0],
                "name":y[1],
                "age":y[2],
                "director":y[3],
                "production":y[4],
                "file":f"static/Filmy/{y[1].replace(' ', '-').replace(':','')}.png"
            })]

    return function(movies = ans,movies2=ans2, title = data.title)
