import mysql.connector as sql
from mysql.connector.connection import MySQLConnection as mysql
from mysql.connector import errorcode
import re
def connection(name="root", passwd="")->mysql:
    try:
        connection = mysql()
        connection.connect(user=name, password=passwd, host='127.0.0.1', database='wypozyczalnia')
    except sql.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    mysql.autocommit = True
    return connection
def check_mail(email)->bool:
    p = re.compile(r"^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$")
    return bool(p.search(email))
def check_injection(tekst)->str:
    p = re.compile(r".* or .*")
    wynik = p.search(tekst)
    if(bool(wynik)):
        return tekst[:- wynik.span()[0]]
    else:
        return tekst
def check_passwd(passwd)->bool:
    return True
def checkdata(connection, typ, wartosc)->int:
    if(type(connection)==sql.connection.MySQLConnection):
        curs = connection.cursor()
    else:
        return -1
    curs.execute(f"SELECT {typ} FROM `uzytkownicy` where {typ} like '{wartosc}';")
    wynik = curs.fetchall()
    curs.close()
    return bool(wynik)
def user_register(connection, login, email, passwd)->int:
    if(type(connection)==sql.connection.MySQLConnection):
        curs = connection.cursor()
    else:
        return -1
    if(type(login)!= str or type(email)!=str or type(passwd)!=str):
        curs.close()
        return -2
    else:
        if(check_mail(email)):
            if(check_passwd(passwd)):
                if(checkdata(conn, "nazwa", login) or checkdata(conn, "email", email) or checkdata(conn, "haslo", passwd)):
                    curs.close()
                    return -5
                else:
                    curs.execute(f"INSERT INTO `uzytkownicy`  VALUES (NULL, '{check_injection(login)}', '{check_injection(email)}', '{check_injection(passwd)}', NULL, NULL, 0);")
                    connection.commit()
                    curs.execute(f"SELECT id_user FROM `uzytkownicy` ORDER BY id_user DESC limit 1;")
                    wynik = curs.fetchall()
                    curs.close()
                    return int(wynik[0][0])
            else:
                curs.close()
                return -4
        else:
            curs.close()
            return -3
def user_login(connection, name, passwd)->int:
    if(type(connection)==sql.connection.MySQLConnection):
        curs = connection.cursor()
    else:
        return -1
    if(type(name)!=str or type(passwd)!=str):
        return -2
    else:
        curs.execute(f"SELECT id_user FROM uzytkownicy WHERE (nazwa LIKE '{check_injection(name)}') or (haslo LIKE '{check_injection(passwd)}')")
        wynik = curs.fetchall()
    if(bool(wynik)):
        curs.close()
        return wynik[0][0]
    else:
        curs.close()
        return -6
conne = connection()
print(user_register(conne, "terminatorek", "terminatorwrzechswiatow@gmail.com", "Graczka"))
print(user_login(conne, "terminatorek", "Graczka"))
conne.close()