import mysql.connector as sql
from mysql.connector.connection import MySQLConnection as mysql
from mysql.connector import errorcode
import re
import modules_user as mu
def wyp_filmy(connection:sql.connection.MySQLConnection, user_id:int)->list:
    curs = connection.cursor()
    curs.execute("Select ")
conn = mu.connection()
