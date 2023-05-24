import sys
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    
    if bottle.request.method == 'POST':
        if bottle.request.forms.get('logout', None) == "Wyloguj":
            bottle.response.set_cookie('id', '', expires=0)
            bottle.response.set_cookie('zal', '', expires=0)
            return redirect('/')
        
    user_id = bottle.request.get_cookie("id")
    
    if user_id:
        user_id = int(user_id)

        user = sql.user_finder(user_id)

        if user.isUsefull():

            rented = sql.user_actual_rent(user_id)
            history = sql.user_rent_history(user_id)
            not_returned = sql.user_have_return(user_id, today())

            admin = False
            if sql.admin(user_id).getBool():
                admin = True

            user_list = user.getList()
            bottle.response.set_cookie('user', str(f"{user_list[1]}|{user_list[2]}|{user_list[3]}"))
            
            rented_list = []
            return_popup = []
            history_list = []

            if rented.isUsefull() and not_returned.isUsefull():
                not_returned = not_returned.getList()

                for x in not_returned:
                    q = sql.movie_finder(int(x[1]))
                    if q.isUsefull():
                        q = q.getList()
                        return_popup.append(f'{q[1]}')

                for x in rented.getList():
                    q = sql.movie_finder(int(x[1]))
                    if q.isUsefull():
                        q = q.getList()
                        rented_list.append(Struct({
                            "id":x[1],
                            "name":q[1],
                            "rent":x[3],
                            "return_date":x[4],
                            "to_return":x in not_returned,
                            "file":f"static/Filmy/{q[1].replace(' ', '-').replace(':','')}.png"
                        }))

            elif rented.isUsefull():

                for x in rented.getList():
                    q = sql.movie_finder(int(x[1]))
                    if q.isUsefull():
                        q = q.getList()
                        rented_list.append(Struct({
                            "id":x[1],
                            "name":q[1],
                            "rent":x[3],
                            "return_date":x[4],
                            "to_return":False,
                            "file":f"static/Filmy/{q[1].replace(' ', '-').replace(':','')}.png"
                        }))
            
            if history.isUsefull():

                for x in history.getList():
                    q = sql.movie_finder(int(x[1]))
                    if q.isUsefull():
                        q = q.getList()
                        history_list.append(Struct({
                            "id":x[1],
                            "name":q[1],
                            "rent":x[3],
                            "return_date":x[4],
                            "real_return":x[5],
                            "file":f"static/Filmy/{q[1].replace(' ', '-').replace(':','')}.png"
                        }))
            return function(user = user_list, rented = rented_list, history = history_list, admin = admin, return_popup = return_popup, **kwg)
        
    return redirect('/logowanie')
