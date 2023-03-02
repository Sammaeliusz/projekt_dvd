import flask
from os import getcwd
from datetime import date, timedelta
from modules import *
import mysql.connector

def index(function:callable):
    #if flask.request.method == 'POST':
        #flask.session['id'] = flask.request.form['id']
        #return flask.redirect(flask.url_for('panel'))
    #return '''
    #    <form method="post">
    #        <p><input type=text name=id></p>
    #        <p><input type=submit value=Login></p>
    #    </form>
    #'''
    return function()

def panel(function:callable) -> callable:
    if 'id' in flask.session:
        id = flask.request.cookies.get("id")
        user = user_finder(conn, id)
        flask.session['user'] = f"{user[1]}|{user[2]}|{user[3]}"
        wyp = wyp_filmy(conn, id)
        swyp = ""
        swypp = ""
        dzisiaj = date.today()
        for i in wyp:
            film = film_finder(conn, i[0])
            if i[3] == None and i[2] != None :
                czy_zalegly = "tak" if i[2]-dzisiaj < timedelta(0) else "nie"
                swyp += f'''
                <tr>
                    <td>{film[1]}</td>
                    <td>{i[1].day}.{i[1].month}.{i[1].year}-{i[2].day}.{i[2].month}.{i[2].year}</td>
                    <td>{czy_zalegly}</td>
                </tr>'''
            elif(i[3]!= None):
                swypp += f'''
                <tr>
                    <td>{film[1]}</td>
                    <td>{i[1].day}.{i[1].month}.{i[1].year}-{i[3].day}.{i[3].month}.{i[3].year}</td>
                </tr>'''
        if flask.request.method == 'POST':
            if (flask.request.form['logout']=="Wyloguj"):
                flask.session.pop('id', None)
                return flask.redirect(flask.url_for('index'))
        return function(user=user, swyp=swyp, swypp=swypp)
    return "Coś nie działa"

def zmiana(function:callable) -> callable:
    try:
        if 'user' in flask.session:
            user = flask.session['user']
            id = flask.request.cookies.get("id")
            user = user.split("|")
        if flask.request.method == 'POST':
            user=["","",""]
            if 'nazwa' in flask.request.form:
                if (n:=flask.request.form['nazwa'])!="":
                    user[0]=n
            if 'mail' in flask.request.form:
                if (n:=flask.request.form['mail'])!="":
                    user[1]=n
            if 'passwd' in flask.request.form:
                if (n:=flask.request.form['passwd'])!="":
                    user[2]=n
            user_change_data(conn, id, user)
            return flask.redirect(flask.url_for('panel'))
    except Exception as err:
        print(err)
    finally:
        return function()

def userclick():
    if flask.request.cookies.get('id') != None:
        return flask.redirect(flask.url_for('panel'))
    else:
        print("asda")
        return flask.redirect(flask.url_for('login'))

def login(function:callable) -> callable:
    try:
        if 'name' in flask.request.form and 'password' in flask.request.form:
            if (n:=flask.request.form['name'])!="" and (n2:=flask.request.form['password'])!="":
                if (id_user:=user_login(conn, n, n2)) > 0:
                    resp  = flask.redirect(flask.url_for('panel'))
                    resp.set_cookie('id', bytes(str(id_user), 'utf-8'))
                    #flask.session['id'] = id_user
                    flask.session['user_auth'] = "placeholder"
                    return resp
                else:
                    return function(error=id_user)
            else:
                return function()
        else:
            return function()
    except Exception as err:
        print(err)
        return function(error=err)

def register(function:callable) -> callable:
    if 'name' in flask.request.form and 'password' in flask.request.form and 'email' in flask.request.form:
        if (n:=flask.request.form['name'])!="" and (n2:=flask.request.form['password'])!="" and (n3:=flask.request.form['email'])!="":
            if (id_user:=user_register(conn, n, n3, n2)) > 0:
                print(id_user)
                flask.session['id'] = id_user
                flask.session['user_auth'] = "placeholder"
                return flask.redirect(flask.url_for('panel'))
            else:
                print(id_user)
                return function(error=id_user)
        else:
            print("?2")
            return function()
    else:
        print("?")
        return function()
