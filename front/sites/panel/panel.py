import sys
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    if bottle.request.method == 'POST':
        if bottle.request.forms.get('logout', None) == "Wyloguj":
            bottle.response.set_cookie('id', '', expires=0)
            return redirect('/')
    us_id = bottle.request.get_cookie("id")
    if us_id:
        print(us_id)
        user = sql.user_finder(us_id)
        if not user.isInfo():
            print(user.list())
            bottle.response.set_cookie('user', str(f"{user.list()[1]}|{user.list()[2]}|{user.list()[3]}"))
            rented = sql.movies_rented(us_id)
            if not rented.isInfo() and rented.hasData():
                rented_history = ""
                rented_history2 = ""
                today = date.today()
                n = 0
                for i in rented.list():
                    movie = sql.movie_finder(i[0])
                    if not movie.isInfo():
                        if i[3] == None and i[2] != None :
                            if i[2]-today < timedelta(0):
                                is_overdue = "tak" 
                                n += 1
                                if bottle.request.get_cookie('zal'):
                                    bottle.response.set_cookie('zal', str("yes"))
                                    return redirect('/panel')
                            else: 
                                is_overdue = "nie"
                            rented_history += f'''
                            <tr class="position">
                                <td class="name">{movie.list()[1]}</td>
                                <td class="data">{i[1].day}.{i[1].month}.{i[1].year}-{i[2].day}.{i[2].month}.{i[2].year}</td>
                                <td class="iss">{is_overdue}</td>
                            </tr>'''
                        elif(i[3]!= None):
                            rented_history2 += f'''
                            <tr class="position">
                                <td class="name">{movie.list()[1]}</td>
                                <td class="data">{i[1].day}.{i[1].month}.{i[1].year}-{i[3].day}.{i[3].month}.{i[3].year}</td>
                            </tr>'''
                    if n == 0 and (m:=bottle.request.get_cookie('zal')):
                        if m == "yes":
                            bottle.response.set_cookie('zal', '', expires=0)
                            return redirect('/panel')
                return function(user=user, swyp=rented_history, swypp=rented_history2, **kwg)
            return function(user=user.list(), swyp="", swypp="", **kwg)
    return redirect('/logowanie')
