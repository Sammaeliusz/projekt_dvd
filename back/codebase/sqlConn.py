import mysql.connector as sql
from mysql.connector.connection import MySQLConnection as mysql
from mysql.connector import errorcode
import re
from sys import stdout
from datetime import datetime as datef
from codebase.uses import Struct, sqlAnswer

basic = {
    "username":"cli",
    "password":"$NaBu6",
    "hostname":"127.0.0.1",
    "databaseName":"wypozyczalnia"
    }

class SQL:

    __codes__ = {}

    def __log__(self, code:int, notes=""):
        self.stream("[{1}] {2} {0} {3}".format(*[*self.__codes__[code], datef.now().strftime("us:%f => %H:%M:%Ss >>>"), f"::: {notes}\n" if len(notes) > 0 else "\n"]))
    
    def __init__(self, username:str, password:str, hostname:str, databaseName:str, stream=stdout.write):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.databaseName = databaseName
        self.stream = stream
        self.connection = mysql()
        self.established = False

        with open('codebase/sql/sql.error', 'r') as f:
            y = [y.split(':') for y in f.readlines()]
            self.__codes__ = {int(x[0]) : [x[1],x[2].replace('\n','')] for x in y}
        
        self.__connect__()

    def __connect__(self) -> bool:
        if not self.connection.is_connected():
            try:
                self.connection = mysql()
                self.connection.connect(user = self.username, password = self.password, host = self.hostname, database = self.databaseName)
                self.__log__(-1001)
                self.established = True
                mysql.autocommit = True
            except sql.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    self.__log__(-100)
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.__log__(-101)
                else:
                    self.__log__(-102, notes=str(err))
                self.established = False
        return self.established

    def cursor(self):
        if not self.__connect__():
            return False
        else:
            return self.connection.cursor()

    def select(self, cursor:sql.cursor.MySQLCursor, command:str) -> list:
        if cursor != False:
            cursor.execute(command)
            return cursor.fetchall()
        else:
            return False

    def distable(self, data:list) -> list:
        if len(data) == 1:
            if len(data[0]) == 1:
                return data[0][0]
            else:
                return data[0]
        return [i[0] if len(i) == 1 else i for i in data]

    def return_id(self, data:list) -> list:
        return [i[0] for i in data]

    def mail_check(self, mail:str) -> bool:
        return bool(re.compile(".+@.+\..+").search(mail))

    def protection(self, question:str) -> str:
        return question[:- answer.span()[0]] if bool(answer:=re.compile(r".* or .*", re.I).search(question)) else question

    def password_check(self, password:str) -> bool:
        return bool(re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$').search(password))

    def userdata_check(self, chap:str, value:str) -> sqlAnswer:
        if(cursor:=self.cursor()):
            answer = self.select(cursor, f"SELECT {chap} FROM `uzytkownicy` where {chap} like '{value}' and status = 0;")
            cursor.close()
            self.__log__(-1002)
            return sqlAnswer(True)
        else:
            self.__log__(-200)
            return sqlAnswer(self.__codes__[-200])

    def inactivity_check(self, user_id:int) -> sqlAnswer:
        if(cursor:=self.cursor()):
            if(answer:=self.select(cursor, f"SELECT status from `uzytkownicy` WHERE id_user = {user_id}") != []):
                cursor.close()
                self.__log__(-1003)
                return sqlAnswer(answer)
            else:
                cursor.close()
                self.__log__(-6, notes=f"user_id -> {user_id}")
                return sqlAnswer(self.__codes__[-6])
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def new_user(self, username:str, mail:str, password:str) -> sqlAnswer:
        if not self.mail_check(mail):
            self.__log__(-1, notes=f"wrong mail provided -> {mail}")
            return sqlAnswer(self.__codes__[-1])
        elif not self.password_check(password):
            self.__log__(-2, notes=f"wrong password provided -> {password}")
            return sqlAnswer(self.__codes__[-2])
        elif not self.userdata_check("email", mail):
            self.__log__(-3, notes=f"registration with mail -> {mail}")
            return sqlAnswer(self.__codes__[-3])
        else:
            if(cursor:=self.cursor()):
                cursor.execute(f"INSERT INTO `uzytkownicy`  VALUES (NULL, '{self.protection(username)}', '{self.protection(mail)}', '{self.protection(password)}', NULL, NULL, 0);")
                self.connection.commit()
                self.__log__(-1004)
                answer = self.select(cursor, f"SELECT id_user FROM `uzytkownicy` ORDER BY id_user DESC limit 1;")
                cursor.close()
                return sqlAnswer(answer)
            else:
                self.__log__(-200)
            return sqlAnswer(self.__codes__[-200])

    def login_user(self, mail:str, password:str) -> sqlAnswer:
        if(cursor:=self.cursor()):
            if not bool(answer:=self.select(cursor, f"SELECT id_user FROM uzytkownicy WHERE (email LIKE '{self.protection(mail)}') and (haslo LIKE '{self.protection(password)}')")):
                cursor.close()
                self.__log__(-4, notes=f"wrond password or/and mail provided -> pass:{password} mail:{mail}")
                return sqlAnswer(self.__codes__[-4])
            elif not self.inactivity_check(answer[0][0]):
                cursor.close()
                self.__log__(-5, notes=f"inactive user id -> {answer[0][0]}")
                return sqlAnswer(self.__codes__[-5])
            else:
                self.__log__(-1005, notes=f"logged user id -> {answer[0][0]}")
                cursor.close()
                return sqlAnswer(answer)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def userdata_change(self, user_id:int, username:str, mail:str, password:str) -> sqlAnswer:
        if(cursor:=self.cursor()):
            if not self.mail_check(mail):
                self.__log__(-1, notes=f"wrong mail provided -> {mail}")
                return sqlAnswer(self.__codes__[-1])
            elif not self.password_check(password):
                self.__log__(-2, notes=f"wrong password provided -> {password}")
                return sqlAnswer(self.__codes__[-2])
            elif not self.userdata_check("email", mail).getBool():
                self.__log__(-3, notes=f"user data change with name -> {username}")
                return sqlAnswer(self.__codes__[-3])
            elif not self.inactivity_check(user_id).getBool:
                self.__log__(-5, notes=f"inactive user id -> {user_id}")
                return sqlAnswer(self.__codes__[-5])
            else:
                cursor.execute(f"UPDATE `uzytkownicy` SET nazwa = '{self.protection(username)}', email = '{self.protection(mail)}', haslo = '{self.protection(password)}' WHERE id_user = {user_id};")
                self.connection.commit()
                cursor.close()
                self.__log__(-1006, notes=f"new user data -> username:{self.protection(username)} mail:{self.protection(mail)} password:{self.protection(password)} :: with an id -> {user_id}")
                return sqlAnswer(True)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def data_delete(self, user_id:int) -> sqlAnswer:
        if(cursor:=self.cursor()):
            cursor.execute(f"UPDATE `uzytkownicy` SET status = 1 WHERE id_user = {user_id}")
            self.connection.commit()
            cursor.close()
            self.__log__(-1007, notes=f"deleted user id -> {user_id}")
            return sqlAnswer(True)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def movies_rented(self, user_id:int) -> sqlAnswer:
        if(cursor:=self.cursor()):
            answer = self.select(cursor, f"SELECT id_film, termin_rent, termin_zwrot, data_zwrot from wypozyczenia where id_user = {user_id}")
            cursor.close()
            self.__log__(-1008, notes=f"of user id -> {user_id}")
            return sqlAnswer(answer)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def movies_add(self, title:str, genre:str, director:str, production:int, age:int) -> sqlAnswer:
        if(production>1995):
            if(cursor:=self.cursor()):
                cursor.execute(f"INSERT INTO `filmy`  VALUES (NULL, '{self.protection(title)}', '{self.protection(genre)}', {age}, '{self.protection(director)}', {production}, True);")
                self.connection.commit()
                cursor.close()
                self.__log__(-1010, notes=f"movie data -> title:{self.protection(title)} genre:{self.protection(genre)} age:{age} director:{self.protection(director)} production_year:{production}")
                return sqlAnswer(True)
            else:
                self.__log__(-200)
            return sqlAnswer(self.__codes__[-200])
        else:
            self.__log__(-7, notes=f"year provided -> {production}")
            return sqlAnswer(self.__codes__[-7])

    def movies_find(self, criterion:str, value:int | str, table:str) -> sqlAnswer:
        if not table in ["filmy", "uzytkownicy", "wypozyczenia"]:
            self.__log__(-8, notes=f"criterion provided -> {criterion}")
            return sqlAnswer(self.__codes__[-8])
        if(cursor:=self.cursor()):
            answer = self.select(cursor, f"SELECT * from `{table}` where {criterion} like {value}") if isinstance(value, int) else self.select(cursor, f"SELECT * from `{table}` where {criterion} like '{value}'")
            cursor.close()
            self.__log__(-1011, notes=f"searched for movies with -> criterion:{criterion} value:{value} :: in table -> {table}")
            return sqlAnswer(answer)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def movie_finder(self, movie_id:int) -> sqlAnswer:
        if(cursor:=self.cursor()):
            answer = self.select(cursor, f"SELECT * from `filmy` where id_film = {movie_id}")
            cursor.close()
            return sqlAnswer(answer)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def user_finder(self, user_id:int) -> sqlAnswer:
        if(cursor:=self.cursor()):
            answer = self.select(cursor, f"SELECT * from `uzytkownicy` where id_user = {user_id}")
            cursor.close()
            return sqlAnswer(answer)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def movice_change(self, movie_id:int, title:str, genre:str, director:str, production:int, age:int) -> sqlAnswer:
        if(cursor:=self.cursor()):
            cursor.execute(f"UPDATE `filmy` SET tytul = '{self.protection(title)}', gatunek = '{self.protection(genre)}', kat_wiek = {age}, rezyser = '{self.protection(director)}', rok_produkcji = {production} WHERE id_film = {movie_id};")
            self.connection.commit()
            cursor.close()
            return sqlAnswer(True)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def movies_recent(self, amount:int) -> sqlAnswer:
        if(cursor:=self.cursor()):
            ids = self.select(cursor, f"select id_film from filmy order by id_film desc limit {amount}")
            cursor.close()
            answer = []
            for x in ids:
                answer.append(self.movie_finder(int(x[0])).list())
            self.__log__(-1009, notes=f"found {amount} recent movies")
            return sqlAnswer(answer)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def film_delete(self, movie_id:int) -> sqlAnswer:
        if(cursor:=self.cursor()):
            cursor.execute(f"UPDATE `filmy` SET dost = False WHERE id_film = {movie_id}")
            self.connection.commit()
            cursor.close()
            return sqlAnswer(True)
        else:
            self.__log__(-200)
        return sqlAnswer(self.__codes__[-200])

    def find_unique(self, category:str, table:str) -> sqlAnswer:
        if not table in ["filmy", "uzytkownicy", "wypozyczenia"]:
            self.__log__(-8, notes=f"category provided -> {category}")
            return sqlAnswer(self.__codes__[-8])
        else:
            if(cursor:=self.cursor()):
                answer = self.select(cursor, f"SELECT {category} FROM {table} GROUP BY {category}")
                cursor.close()
                return sqlAnswer(answer)
            else:
                self.__log__(-200)
            return sqlAnswer(self.__codes__[-200])
        
            
