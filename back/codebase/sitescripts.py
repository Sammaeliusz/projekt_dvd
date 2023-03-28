import bottle
from os import getcwd
from datetime import date, timedelta
from codebase.modules import *
import mysql.connector
from io import BytesIO

def redirect(location:str) -> bottle.Response:
    try:
        return bottle.redirect(location)
    except bottle.HTTPResponse as res:
        return res
        
    #return bottle.Response(body="amogus", headers={'Location':location}, status_code=301)

def environhack():
    body = "amogus"
    bottle.request.environ['CONTENT_LENGTH'] = str(len(bottle.tob(body)))
    bottle.request.environ['wsgi.input'] = BytesIO()
    bottle.request.environ['wsgi.input'].write(bottle.tob(body))
    bottle.request.environ['wsgi.input'].seek(0)

def index(function:callable):
    return function()

def panel(function:callable) -> callable:
    environhack()
    us_id = bottle.request.get_cookie("id")
    if us_id:
        user = user_finder(conn, us_id)
        bottle.response.set_cookie('user', bytes(str(f"{user[1]}|{user[2]}|{user[3]}"), 'utf-8'))
        rented = wyp_filmy(conn, us_id)
        rented_history = ""
        rented_history2 = ""
        today = date.today()
        n = 0
        for i in rented:
            movie = film_finder(conn, i[0])
            if i[3] == None and i[2] != None :
                if i[2]-today < timedelta(0):
                    is_overdue = "tak" 
                    n += 1
                    if bottle.request.get_cookie('zal'):
                        bottle.response.set_cookie('zal', bytes(str("yes"), 'utf-8'))
                        return redirect('/panel')
                else: 
                    is_overdue = "nie"
                rented_history += f'''
                <tr>
                    <td>{film[1]}</td>
                    <td>{i[1].day}.{i[1].month}.{i[1].year}-{i[2].day}.{i[2].month}.{i[2].year}</td>
                    <td>{czy_zalegly}</td>
                </tr>'''
            elif(i[3]!= None):
                rented_history2 += f'''
                <tr>
                    <td>{film[1]}</td>
                    <td>{i[1].day}.{i[1].month}.{i[1].year}-{i[3].day}.{i[3].month}.{i[3].year}</td>
                </tr>'''
        if n == 0 and (m:=bottle.request.get_cookie('zal')):
            if m == "yes":
                bottle.response.set_cookie('zal', '', expires=0)
                return redirect('/panel')
        if bottle.request.method == 'POST':
            if bottle.request.forms.get('logout', None) == "Wyloguj":
                bottle.response.set_cookie('id', '', expires=0)
                return redirect('/')
        return function(user=user, swyp=rented_history, swypp=rented_history2)
    return redirect('/logowanie')

def zmiana(function:callable) -> callable:
    if (user:=bottle.request.get_cookie("user")):
        user = user.split("|")
        if bottle.request.method == 'POST':
            if (e:=user_change_data(conn, bottle.request.get_cookie("id"), [x if x != None else user[n] for n, x in enumerate([bottle.request.forms.get('name', None),bottle.request.forms.get('mail', None),bottle.request.forms.get('passwd', None)])])) < 0:
                return function(error=e)
            else:
                return redirect('/panel')
    return function(error=None)

def userclick():
    if bottle.request.get_cookie('id'):
        return redirect('/panel')
    else:
        return redirect('/logowanie')

def login(function:callable) -> callable:
    environhack()
    if (mail:=bottle.request.forms.get('mail', None)) and (password:=bottle.request.forms.get('password', None)):
        if (id_user:=user_login(conn, mail, password)) > 0:
            bottle.response.set_cookie('id', bytes(str(id_user), 'utf-8'))
            bottle.request.set_cookie("user_auth", "placeholder")
            return redirect('/panel')
        else:
            return function(error=id_user)
    else:
        return function()

def register(function:callable) -> callable:
    environhack()
    if (mail:=bottle.request.forms.get('mail', None)) and (password:=bottle.request.forms.get('password', None)) and (name:=bottle.request.forms.get('name', None)):
        if (id_user:=user_register(conn, name, mail, password)) > 0:
            bottle.response.set_cookie('id', bytes(str(id_user), 'utf-8'))
            bottle.request.set_cookie("user_auth", "placeholder")
            return redirect('/panel')
        else:
            print(id_user)
            return function(error=id_user)
    else:
        print(id_user)
        return function(error=None)
    
def zbiory(function:callable) -> callable:
    return function()

funclist = {
    "index":index,
    "panel":panel,
    "zmiana":zmiana,
    "userclick":userclick,
    "login":login,
    "register":register,
    "zbiory":zbiory,
    }
