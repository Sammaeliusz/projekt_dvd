import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    question = sql.movie_finder(int(bottle.request.query['mid']))
    if question.isUsefull():
        return function(movie=question.getList())
    return redirect('/')
