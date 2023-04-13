import sys
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    
    if bottle.request.method == 'POST':
        if bottle.request.forms.get('logout', None) == "Wyloguj":
            bottle.response.set_cookie('id', '', expires=0)
            bottle.response.set_cookie('zal', '', expires=0)
            return redirect('/')
        
    us_id = bottle.request.get_cookie("id")
    
    if us_id:
        user = sql.user_finder(us_id)
        if sql.admin(us_id).getList()[0]==2:
            lin = """<button onclick="window.location.href = '/admin'">Przejdź do panelu Admina</button>"""
        else:
            lin = ""
        if user.isUsefull():
            bottle.response.set_cookie('user', str(f"{user.getList()[1]}|{user.getList()[2]}|{user.getList()[3]}"))
            rented = sql.movies_rented(us_id)
            
            if rented.isUsefull():
                rented_history = ""
                rented_history2 = ""
                today = date.today()
                n = 0
                rlist = rented.getList()
                if not isinstance(rlist[0], list):
                    rlist = [rlist]

                for i in rlist:
                    print(i)
                    movie = sql.movie_finder(i[0])
                    print(movie.getList())
                    if movie.isUsefull():
                        
                        if i[3] == None and i[2] != None:
                                
                            if i[2]-today < timedelta(0):
                                is_overdue = "tak"
                                n += 1
                                if bottle.request.get_cookie('zal')!="yes":
                                    bottle.response.set_cookie('zal', str("yes"))
                                    return redirect('/panel')
                            else: 
                                is_overdue = "nie"
                                
                            rented_history += f'''
                            <tr class="position">
                                <td class="name">{movie.getList()[1]}</td>
                                <td class="data">{i[1].day}.{i[1].month}.{i[1].year}-{i[2].day}.{i[2].month}.{i[2].year}</td>
                                <td class="iss">{is_overdue}</td>
                            </tr>'''
                            
                        elif(i[3]!= None):
                            
                            rented_history2 += f'''
                            <tr class="position">
                                <td class="name">{movie.getList()[1]}</td>
                                <td class="data">{i[1].day}.{i[1].month}.{i[1].year}-{i[3].day}.{i[3].month}.{i[3].year}</td>
                            </tr>'''
                            is_overdue="nie"
                return function(user=user.getList(), swyp=rented_history, swypp=rented_history2,admin= lin, **kwg)
            
            return function(user=user.getList(), swyp="", swypp="", admin= lin, **kwg)
        
    return redirect('/logowanie')
