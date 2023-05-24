import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:

    movie_id = int(bottle.request.query['mid'])
    question = sql.movie_finder(movie_id)
    rent_error = 0
    not_rented = True

    if bottle.request.method == 'POST':
        if bottle.request.forms.get('rent', None) == str(movie_id):
            
            rent_error = 1
            user_id = bottle.request.get_cookie("id")
            if user_id:
                user_id = int(user_id)

                user = sql.user_finder(user_id)

                if user.isUsefull():
                    q = sql.rent(movie_id, user_id, today(), today_add(days=14))

                    if q.isUsefull():
                        rent_error = 2


    if not question.isUsefull():
        return redirect('/')

    tags = sql.movie_tags(movie_id)

    if tags.isError() or tags.isInfo():
        sql.__log__(-10001, notes = f'{tags.getMessage()}')
        return function(movie=question.getList(), tags=[])
    
    user_id = bottle.request.get_cookie("id")
    
    if user_id:
        user_id = int(user_id)

        user = sql.user_finder(user_id)

        if user.isUsefull():
            q = sql.user_actual_rent(user_id)
            if q.isUsefull():
                q = q.getList()
                if not isinstance(q[0],list):
                    q = [q]
                for x in q:
                    if x[1] == movie_id:
                        not_rented = False
                        break

    return function(movie=question.getList(), tags=tags.getList(), re = rent_error, not_rented = not_rented)
