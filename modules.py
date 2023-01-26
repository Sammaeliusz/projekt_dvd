import mysql.connector as sql
import re
def connection(name="root", passwd="")->sql.connection:
    connection = sql.connect(user=name, password=passwd, host='127.0.0.1', database='wypozyczalnia')
    sql.autocommit = True
    return connection
def check_mail(email)->bool:
    p = re.compile(r"^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$")
    return bool(p.search(email))
def check_injection(tekst)->str:
    p = re.compile(r"* or *")
    if(bool(p.search(tekst))):
        return tekst[:- p.search(tekst).span()[0]]
    else:
        return tekst
def check_passwd(passwd)->bool:
    return True
def checkdata(conn, typ, wartosc)->int:
    if(type(conn)==sql.connection):
        curs = conn.cursor()
    else:
        curs.close()
        return -1
    curs.execute(f"SELECT {typ} FROM `uzytkownicy` where {typ} like '{wartosc}';")
    wynik = curs.fetchall()
    curs.close()
    return bool(wynik)
def user_register(conn, login, email, passwd)->int:
    if(type(conn)==sql.connection):
        curs = conn.cursor()
    else:
        curs.close()
        return -1
    if(type(login)!= str or type(email)!=str or type(passwd)!=str):
        curs.close()
        return -2
    else:
        if(check_mail(email)):
            if(check_passwd(passwd)):
                if(checkdata(conn, "nazwa", login) or checkdata(conn, "email", email) or checkdata(conn, "haslo", passwd)):
                    curs.execute(f"INSERT INTO `uzytkownicy`  VALUES (NULL, '{check_injection(login)}', '{check_injection(email)}', '{check_injection(passwd)}', NULL, NULL, 0);")
                    curs.execute(f"SELECT id_user FROM `uzytkownicy` ORDER BY id_user DESC limit 1;")
                    wynik = curs.fetchall()
                    curs.close()
                    return int(wynik[0])
                else:
                    curs.close()
                    return -5
            else:
                curs.close()
                return -4
        else:
            curs.close()
            return -3
def user_login(conn, name, passwd)->int:
    if(type(conn)==sql.connection):
        curs = conn.cursor()
    else:
        return -1
    if(type(name)!=str or type(passwd)!=str):
        return -2
    else:
        curs.execute(f"SELECT id_user FROM uzytkownicy WHERE (nazwa LIKE '{check_injection(name)}') or (haslo LIKE '{check_injection(passwd)}')")
        wynik = curs.fetchall()
    if(bool(wynik)):
        curs.close()
        return -6
    else:
        curs.close()
        return wynik
conn = connection()

conn.close()