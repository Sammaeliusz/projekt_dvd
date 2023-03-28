import sys
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    #environhack()
    us_id = bottle.request.get_cookie("id")
    if us_id:
        user = sql.user_finder(us_id)[0]
        bottle.response.set_cookie('user', str(f"{user[1]}|{user[2]}|{user[3]}"))
        rented = sql.movies_rented(us_id)
        rented_history = ""
        rented_history2 = ""
        today = date.today()
        n = 0
        for i in rented:
            movie = sql.movie_finder(i[0])
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
                    <td class="name">{film[1]}</td>
                    <td class="data">{i[1].day}.{i[1].month}.{i[1].year}-{i[2].day}.{i[2].month}.{i[2].year}</td>
                    <td class="iss">{czy_zalegly}</td>
                </tr>'''
            elif(i[3]!= None):
                rented_history2 += f'''
                <tr class="position">
                    <td class="name">{film[1]}</td>
                    <td class="data">{i[1].day}.{i[1].month}.{i[1].year}-{i[3].day}.{i[3].month}.{i[3].year}</td>
                </tr>'''
        if n == 0 and (m:=bottle.request.get_cookie('zal')):
            if m == "yes":
                bottle.response.set_cookie('zal', '', expires=0)
                return redirect('/panel')
        if bottle.request.method == 'POST':
            if bottle.request.forms.get('logout', None) == "Wyloguj":
                bottle.response.set_cookie('id', '', expires=0)
                return redirect('/')
        return function(user=user, swyp=rented_history, swypp=rented_history2, **kwg)
    return redirect('/logowanie')
