import mysql.connector as sql
from mysql.connector.connection import MySQLConnection as mysql
from mysql.connector import errorcode
import re
import modules_user as mu
def wyp_filmy(connection:sql.connection.MySQLConnection, user_id:int)->list:
    curs = connection.cursor()
    curs.execute("Select ")
def ost_dod(connection:sql.connection.MySQLConnection, ilosc:int)->list:
    curs = connection.cursor()
    w = curs.execute(f"Select tytul from filmy order by id desc limit {ilosc}")
    wynik = w.fetchall()
    return wynik
conn = mu.connection()
ost_dod(conn, 5)