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
    t=[]
    tags = sql.movie_tags(movie_id)
    print(tags.getList()[1])
    if tags.isError() or tags.isInfo():
        sql.__log__(-10001, notes = f'{tags.getMessage()}')
        return function(movie=question.getList(), tags=[])
    else:
        tg = tags.getList()
        if isinstance(tg[1],list):
            for i in tg:
                print(i)
                t.append(i[1])
        else:
            t.append(tg[1])
    user_id = bottle.request.get_cookie("id")
    
    if user_id:
        user_id = int(user_id)
        logged=True
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
    else:
        logged=False

    return function(movie=question.getList(), tags=t, re = rent_error, not_rented = not_rented, logged=logged)
