import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    movie_id = int(bottle.request.query['mid'])
    question = sql.movie_finder(movie_id)
    if not question.isUsefull():
        return redirect('/')
    tags = sql.movie_tags(movie_id)
    if tags.isError() or tags.isInfo():
        sql.__log__(-10001, notes = f'{tags.getMessage()}')
        return function(movie=question.getList(), tags=[])
    return function(movie=question.getList(), tags=tags.getList())
