import mysql.connector as sql
from mysql.connector.connection import MySQLConnection as mysql
from mysql.connector import errorcode

import re
from sys import stdout
from datetime import datetime as datef
from datetime import timedelta as timed

from ..SQL.answer import Answer
from ..Error.error import MessageCreator, Error, Info
from ..Tools.structure import Struct
from ..Tools.log import loggingSession as logSes


#SQL class
class SQL:

    __codes__:      dict
    username:       str
    password:       str
    hostname:       str
    dbName:         str
    stream:         callable
    established:    bool


    #Return to the stream message
    def __log__(self, code:int, notes=""):
        self.logSes.log(Struct({"type":self.__codes__[code].getType(), "message":self.__codes__[code].getMessage(), "notes":f"::: {notes}" if len(notes) > 0 else ""}))


    #initializer
    def __init__(self, username:str, password:str, hostname:str, databaseName:str, stream=stdout.write, **data):

        self.username = username
        self.password = password
        self.hostname = hostname
        self.dbName = databaseName
        self.connection = mysql()
        self.established = False

        self.logSes = logSes('SQL', 10, "[{type}] {message} {notes}", stream, Struct({"type":"ERROR", "message":"no message", "notes":""}))

        with open('codebase/Error/sql.error', 'r') as f:
            y = [y.split(':') for y in f.readlines()]
            self.__codes__ = {int(x[0]) : MessageCreator(int(x[0]),message=x[1],typ=x[2].replace('\n','')) for x in y}
        
        self.__connect__()


    #checks if connection is established and tries to connect if not
    def __connect__(self) -> bool:
        
        if not self.connection.is_connected():
            
            try:
                self.connection = mysql()
                self.connection.connect(user = self.username, password = self.password, host = self.hostname, database = self.dbName)
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


    #Get cursor for a function
    #   None if no connection
    def cursor(self):
        
        if not self.__connect__():
            return None
        
        else:
            return self.connection.cursor()


    #wrapper for SELECT
    def execute(self, cursor:sql.cursor.MySQLCursor, command:str) -> list:
        
        if cursor:
            cursor.execute(command)
            return cursor.fetchall()
        
        else:
            return None


    #deprived function for trimming lists
    def distable(self, data:list) -> list:
        if len(data) == 1:
            if len(data[0]) == 1:
                return data[0][0]
            else:
                return data[0]
        return [i[0] if len(i) == 1 else i for i in data]


    #deprived function for getting id from querry
    def return_id(self, data:list) -> list:
        
        return [i[0] for i in data]


    #regex check for valid email
    def mail_check(self, mail:str) -> bool:
        
        return bool(re.compile(".+@.+\..+").search(mail))


    #regex check for SQL injection
    def protection(self, question:str) -> str:
        
        return question[:- answer.span()[0]] if bool(answer:=re.compile(r".* or .*|.*%.*", re.I).search(question)) else question


    #regex check for valid password
    def password_check(self, password:str) -> bool:
        
        return bool(re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$').search(password))


    #checks if data is valid
    def userdata_check(self, typ:str, value:str) -> Answer:
        
        if(cursor:=self.cursor()):
            answer = self.execute(cursor, f"SELECT {typ} FROM `user` WHERE {typ} LIKE '{value}' AND active = 1;")
            cursor.close()
            self.__log__(-1002)
            return Answer(answer)
        
        else:
            self.__log__(-200)
            return Answer(self.__codes__[-200])


    #checks if user is active
    def inactivity_check(self, user_id:int) -> Answer:
        
        if(cursor:=self.cursor()):
            if(answer:=self.execute(cursor, f"SELECT active FROM `user` WHERE id = {user_id}")):
                cursor.close()
                self.__log__(-1003)
                return Answer(answer)
            
            else:
                cursor.close()
                self.__log__(-6, notes=f"user_id -> {user_id}")
                return Answer(self.__codes__[-6])
            
        else:
            self.__log__(-200)
            
        return Answer(self.__codes__[-200])

    def user_unban(self, user_id:int) -> Answer:
        
        if(cursor:=self.cursor()):
            cursor.execute(f"UPDATE `user` SET active = 1 WHERE id = {user_id};")
            self.connection.commit()
            cursor.close()
            self.__log__(-1007, notes=f"activated user id -> {user_id}")
            return Answer(True)
        
        else:
            self.__log__(-200)
            
        return Answer(self.__codes__[-200])
    #creates new user to database
    def new_user(self, username:str, mail:str, password:str, admin=False) -> Answer:
        
        if not self.mail_check(mail):
            self.__log__(-1, notes=f"wrong mail provided -> {mail}")
            return Answer(self.__codes__[-1])
        
        elif not self.password_check(password):
            self.__log__(-2, notes=f"wrong password provided -> {password}")
            return Answer(self.__codes__[-2])
        
        elif not self.userdata_check("mail", mail):
            self.__log__(-3, notes=f"registration with mail -> {mail}")
            return Answer(self.__codes__[-3])
        
        else:
            if(cursor:=self.cursor()):
                privilages = '0'*64
                
                if admin:
                    privilages[63]='1'
                    
                cursor.execute(f"INSERT INTO `user`  VALUES (NULL, '{self.protection(username)}', '{self.protection(mail)}', '{self.protection(password)}', 0, 1, b'{privilages}');")
                self.connection.commit()
                self.__log__(-1004)
                answer = self.execute(cursor, f"SELECT id FROM `user` ORDER BY id DESC LIMIT 1;")
                cursor.close()
                return Answer(answer)
            
            else:
                self.__log__(-200)
                
            return Answer(self.__codes__[-200])


    #checks if data provided is valid and user can be logged in
    #    returns data of user
    def login_user(self, mail:str, password:str) -> Answer:
        
        if(cursor:=self.cursor()):
            answer = Answer(self.execute(cursor, f"SELECT id FROM `user` WHERE (mail LIKE '{self.protection(mail)}') AND (password LIKE '{self.protection(password)}');"))
            if not answer.isUsefull():
                cursor.close()
                self.__log__(-4, notes=f"wrond password or/and mail provided -> pass:{password} mail:{mail}")
                return Answer(self.__codes__[-4])
            
            elif self.inactivity_check(answer.getId()).getList()[0]!=1:
                cursor.close()
                self.__log__(-5, notes=f"inactive user id -> {answer.getId()}")
                return Answer(self.__codes__[-5])
            
            else:
                self.__log__(-1005, notes=f"logged user id -> {answer.getId()}")
                cursor.close()
                return answer
            
        else:
            self.__log__(-200)
            
        return Answer(self.__codes__[-200])


    #changes data of a user
    def userdata_change(self, user_id:int, username:str, mail:str, password:str) -> Answer:
        
        if(cursor:=self.cursor()):
            if not self.mail_check(mail):
                self.__log__(-1, notes=f"wrong mail provided -> {mail}")
                return Answer(self.__codes__[-1])
            
            elif not self.password_check(password):
                self.__log__(-2, notes=f"wrong password provided -> {password}")
                return Answer(self.__codes__[-2])
            
            elif not self.userdata_check("mail", mail).getBool():
                self.__log__(-3, notes=f"user data change with name -> {username}")
                return Answer(self.__codes__[-3])
            
            elif not self.inactivity_check(user_id).getBool:
                self.__log__(-5, notes=f"inactive user id -> {user_id}")
                return Answer(self.__codes__[-5])
            
            cursor.execute(f"UPDATE `user` SET username = '{self.protection(username)}', mail = '{self.protection(mail)}', password = '{self.protection(password)}' WHERE id = {user_id};")
            self.connection.commit()
            cursor.close()
            self.__log__(-1006, notes=f"new user data -> username:{self.protection(username)} mail:{self.protection(mail)} password:{self.protection(password)} :: with an id -> {user_id}")
            return Answer(True)
        
        else:
            self.__log__(-200)
            
        return Answer(self.__codes__[-200])


    #deletes user, by setting his activity status to False
    def user_delete(self, user_id:int) -> Answer:
        
        if(cursor:=self.cursor()):
            cursor.execute(f"UPDATE `user` SET active = 0 WHERE id = {user_id};")
            self.connection.commit()
            cursor.close()
            self.__log__(-1007, notes=f"deactivated user id -> {user_id}")
            return Answer(True)
        
        else:
            self.__log__(-200)
            
        return Answer(self.__codes__[-200])

    def activeUser(self) -> Answer:
        if(cursor:=self.cursor()):
            ans = cursor.execute(f"Select * from user where active = 1")
            cursor.close()
            return Answer(ans)
    #gets movies rented by the user
    def movies_rented(self, user_id:int) -> Answer:
        
        if(cursor:=self.cursor()):
            answer = self.execute(cursor, f"SELECT `movie`, `rent`, `return`, `real_return` FROM `rents` WHERE user = {user_id};")
            cursor.close()
            self.__log__(-1008, notes=f"of user id -> {user_id}")
            return Answer(answer)
        
        else:
            self.__log__(-200)
            
        return Answer(self.__codes__[-200])


    #Adds a movie to database
    def movie_add(self, title:str, tags:str, age:int, director:str, production:int, stock:int, description="") -> Answer:
        
        if(int(production)>1995):
            if(cursor:=self.cursor()):
                cursor.execute(f"INSERT INTO `movie`  VALUES (NULL, '{self.protection(title)}', '{self.protection(tags)}', {age}, '{self.protection(director)}', {production}, {stock}, '{self.protection(description)}');")
                self.connection.commit()
                cursor.close()
                self.__log__(-1010, notes=f"movie data -> title:{self.protection(title)} tags:{self.protection(tags)} age:{age} director:{self.protection(director)} production_year:{production}")
                return Answer(True)
            
            self.__log__(-200)    
            return Answer(self.__codes__[-200])

        self.__log__(-7, notes=f"year provided -> {production}")
        return Answer(self.__codes__[-7])


    #Searches database for a movie by given criterion
    #
    #   !!!TO BE DONE!!!
    #
    def movies_find(self, tags:str, value:int | str) -> Answer:
        return Answer(False)
    
        if(cursor:=self.cursor()):
            answer = self.execute(cursor, f"SELECT * FROM `movie` WHERE {tags} LIKE {value}") if isinstance(value, int) else self.execute(cursor, f"SELECT * FROM `movie` WHERE {criterion} LIKE '{value}'")
            cursor.close()
            self.__log__(-1011, notes=f"searched for movies with -> criterion:{criterion} value:{value} :: in table -> {table}")
            return Answer(answer)
        
        self.__log__(-200)
        return Answer(self.__codes__[-200])


    #Searches for a movie by id
    def movie_finder(self, movie_id:int) -> Answer:
        
        if(cursor:=self.cursor()):
            answer = self.execute(cursor, f"SELECT * FROM `movie` WHERE id = {movie_id}")
            cursor.close()
            return Answer(answer)
        
        self.__log__(-200)
        return Answer(self.__codes__[-200])


    #Searches for a user by id
    def user_finder(self, user_id:int) -> Answer:
        
        if(cursor:=self.cursor()):
            answer = self.execute(cursor, f"SELECT * FROM `user` where id = {user_id}")
            cursor.close()
            return Answer(answer)

        self.__log__(-200)
        return Answer(self.__codes__[-200])


    #Changes data of a movie
    #
    #   TO BE UPDATED
    #
    def movie_change(self, movie_id:int, title:str, genre:str, age:int, director:str, production:int, stock:int, desctiption:str) -> Answer:
        if(cursor:=self.cursor()):
            cursor.execute(f"UPDATE `movie` SET title = '{self.protection(title)}', tags = '{self.protection(genre)}', age = {age}, director = '{self.protection(director)}', production = {production}, stock={stock}, description='{self.protection(desctiption)}' WHERE id = {movie_id};")
            self.connection.commit()
            cursor.close()
            return Answer(True)

        self.__log__(-200)
        return Answer(self.__codes__[-200])


    #Gets recently added movies
    def movies_recent(self, amount:int) -> Answer:
        
        if(cursor:=self.cursor()):
            ids = self.execute(cursor, f"SELECT id FROM movie ORDER BY id DESC LIMIT {amount}")
            cursor.close()
            answer = []
            
            for x in ids:
                answer.append(self.movie_finder(int(x[0])).getList())
                
            self.__log__(-1009, notes=f"found {amount} recent movies")
            return Answer(answer)
        
        self.__log__(-200)
        return Answer(self.__codes__[-200])


    #set stock amout of movie by id
    def movie_delete(self, movie_id:int) -> Answer:
        
        if(cursor:=self.cursor()):
            cursor.execute(f"DELETE FROM `movie` WHERE id = {movie_id}")
            self.connection.commit()
            cursor.close()
            return Answer(True)

        self.__log__(-200)
        return Answer(self.__codes__[-200])


    #actually, I don't know why this even exists
    def all_from_all(self, table:str) -> Answer:
        
        if not table in ["movie", "user", "rent", "tags"]:
            self.__log__(-8, notes=f"not good table name")
            return Answer(self.__codes__[-8])
        
        if(cursor:=self.cursor()):
            answer = self.execute(cursor, f"SELECT * FROM {table}")
            cursor.close()
            return Answer(answer)

        self.__log__(-200)
        return Answer(self.__codes__[-200])
    def getStatus(self, id:int) ->Answer:
            if(cursor:=self.cursor()):
                answer = self.execute(cursor, f"Select active from user where id = {id}")
                cursor.close()
                return Answer(answer)
            else:
                self.__log__(-200)
    def admin(self, id:int) -> Answer:
        if(cursor:=self.cursor()):
            answer = self.execute(cursor, f"Select privilages from user where id = {id}")
            cursor.close()
            print(answer)
            return Answer(answer)
        else:
            self.__log__(-200)       
    def rent(self, id_u:int, id_f:int)->Answer:
        date = datef.today().date()
        if(cursor:=self.cursor()):
            nstock = self.execute(cursor, f"select stock from movie where id={id_f}")
            if nstock.isUsefull:
                nstock -= 1
                self.execute(cursor, f"insert into rents values (Null, {id_f}, {id_u}, {date}, {date+timed(14)}, Null )")
                self.execute(cursor, f"update movie set stock={nstock} where {id_f}")
            cursor.close()
            return Answer(True)
        else:
            self.__log__(-200)
    def deRent(self, id_r:int, id_f:int)->Answer:
        date = datef.today().date()
        if(cursor:=self.cursor()):
            nstock = self.execute(cursor, f"select stock from movie where id={id_f}")
            if nstock.isUsefull:
                nstock += 1
                self.execute(cursor, f"update rents set real_return={date} where id={id_r}")
                self.execute(cursor, f"update movie set stock={nstock} where {id_f}")
            cursor.close()
            return Answer(True)
        else:
            self.__log__(-200)