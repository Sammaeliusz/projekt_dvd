import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    
    title = bottle.request.forms.get('title', None)

    tags = sql.movie_all_tags()
    tag_list = []
    if tags.isUsefull():
        for x in tags.getList():
            tag_list.append([x[1],x[2]])
    
    return function(tags = tag_list, title = title)
