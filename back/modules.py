import mysql.connector as sql
from mysql.connector.connection import MySQLConnection as mysql
from mysql.connector import errorcode
import re
def connection(name="serw", passwd="$dn%g6ACRm8")->mysql:
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
def distable(dane:list)->list:
    w = []
    for i in dane:
        if(len(i)==1):
            w.append(i[0])
        else:
            w.append(i)
    return w
def check_mail(email:str)->bool:
    p = re.compile(r"^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$")
    return bool(p.search(email))
def check_injection(tekst:str)->str:
    p = re.compile(r".* or .*")
    wynik = p.search(tekst)
    if(bool(wynik)):
        return tekst[:- wynik.span()[0]]
    else:
        return tekst
def check_passwd(passwd:str)->bool:
    return True
def checkdata(connection:sql.connection.MySQLConnection, typ:str, wartosc:str)->bool:
    curs = connection.cursor()
    curs.execute(f"SELECT {typ} FROM `uzytkownicy` where {typ} like '{wartosc} and status = 0';")
    wynik = curs.fetchall()
    curs.close()
    return bool(wynik)
def check_activity(connection:sql.connection.MySQLConnection, user_id:int)->int:
    curs = connection.cursor()
    curs.execute(f"SELECT status from `uzytkownicy` WHERE id_user = {user_id}")
    wynik = curs.fetchall()
    curs.close()
    if(wynik != []):
        return wynik[0][0]
    else:
        return -6
def user_register(connection:sql.connection.MySQLConnection, login:str, email:str, passwd:str)->int:
    curs = connection.cursor()
    if(check_mail(email)):
        if(check_passwd(passwd)):
            if(checkdata(connection, "nazwa", login) or checkdata(connection, "email", email)):
                curs.close()
                return -3
            else:
                curs.execute(f"INSERT INTO `uzytkownicy`  VALUES (NULL, '{check_injection(login)}', '{check_injection(email)}', '{check_injection(passwd)}', NULL, NULL, 0);")
                connection.commit()
                curs.execute(f"SELECT id_user FROM `uzytkownicy` ORDER BY id_user DESC limit 1;")
                wynik = curs.fetchall()
                curs.close()
                return int(wynik[0][0])
        else:
            curs.close()
            return -2
    else:
        curs.close()
        return -1
def user_login(connection:sql.connection.MySQLConnection, mail:str, passwd:str)->int:
    curs = connection.cursor()
    curs.execute(f"SELECT id_user FROM uzytkownicy WHERE (email LIKE '{check_injection(mail)}') or (haslo LIKE '{check_injection(passwd)}')")
    wynik = curs.fetchall()
    if(bool(wynik)):
        if(check_activity(connection, wynik[0][0])==0):
            curs.close()
            return wynik[0][0]
        else:
            curs.close()
            return -5
    else:
        curs.close()
        return -4
def user_change_data(connection:sql.connection.MySQLConnection, user_id:int, data:list)->int:
    curs = connection.cursor()
    if(check_activity(connection, user_id)==0):
        if(check_mail(data[1])):
            if(check_passwd([data[2]])):
                if(checkdata(connection, "nazwa", data[0]) or checkdata(connection, "email", data[1])):
                    curs.close()
                    return -3
                else:
                    curs.execute(f"UPDATE `uzytkownicy` SET nazwa = '{check_injection(data[0])}', email = '{check_injection(data[1])}', haslo= '{check_injection(data[2])}' WHERE id_user = {user_id};")
                    connection.commit()
                    curs.close()
                    return 1
            else:
                curs.close()
                return -2
        else:
            curs.close()
            return -1
    else:
        curs.close()
        return -5
def del_data(connection:sql.connection.MySQLConnection, user_id:int)->int:
    curs = connection.cursor()
    curs.execute(f"UPDATE `uzytkownicy` SET status = 1 WHERE id_user = {user_id}")
    connection.commit()
    curs.fetchall()
    curs.close()
    return 1
def wyp_filmy(connection:sql.connection.MySQLConnection, user_id:int)->list:
    curs = connection.cursor()
    curs.execute("Select ")
def ost_dod(connection:sql.connection.MySQLConnection, ilosc:int)->list:
    curs = connection.cursor()
    curs.execute(f"Select tytul from filmy order by id_film desc limit {ilosc}")
    wynik = curs.fetchall()
    return distable(wynik)
def add_film(connection:sql.connection.MySQLConnection, tytul:str, gatunek:str, rezyser:str, rok_prod:int)->int:
    curs = connection.cursor()
    if(rok_prod>1995):
        curs.execute(f"INSERT INTO `filmy`  VALUES (NULL, '{check_injection(tytul)}', '{check_injection(gatunek)}', '{check_injection(rezyser)}', {rok_prod});")
        connection.commit()
        curs.execute(f"SELECT id_film FROM `filmy` ORDER BY id_film DESC limit 1;")
        wynik = curs.fetchall()
        curs.close()
        return int(wynik[0][0])
    else:
        curs.close()
        return -7
conn = connection("root", "")
add_film(conn, "Finding Jesus", "Animacja", "God", 2005)
print(ost_dod(conn, 5))