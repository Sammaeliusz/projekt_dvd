import mysql.connector as sql
from mysql.connector.connection import MySQLConnection as mysql
from mysql.connector import errorcode

import re
from sys import stdout
from datetime import datetime as datef
import tomllib

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

        with open('codebase/SQL/templates/listing.toml', 'rb') as listing:
            confs = tomllib.load(listing)
            with open(f'codebase/SQL/templates/{sorted(list(zip(*[confs["main"]["list"],confs["main"]["priority"]])),key=lambda n: n[1])[-1][0]}', 'rb') as f:
                self.sql_conf = Struct(tomllib.load(f))
                    
            
        
        self.dbName = self.sql_conf.main.dbname
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
                self.__log__(-7)
                self.established = True
                mysql.autocommit = True
                
            except sql.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    self.__log__(-1)
                    
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.__log__(-2)
                    
                else:
                    self.__log__(-10, notes=str(err))
                    
                self.established = False
                
        return self.established

    def logret(self, code:int, notes="") -> Answer:
        self.__log__(code, notes = notes)
        return Answer(self.__codes__[code])


    #Get cursor for a function
    #   None if no connection
    def cursor(self):
        
        if not self.__connect__():
            return None
        
        else:
            return self.connection.cursor()
    
    def date(self, year, month, day) -> str:
        y = str(year)
        if len(str(day)) == 1:
            d = '0'+str(day)
        else:
            d = str(day)
        if len(str(month)) == 1:
            m = '0'+str(month)
        else:
            m = str(month)
        return f'{y}-{m}-{d}'


    #wrapper for SELECT
    def select(self, command:str) -> Answer:
        
        if (cursor:=self.cursor()):
            cursor.execute(command)
            ret = cursor.fetchall()
            cursor.close()
            return Answer(ret)
        
        else:
            return self.logret(-3)

    def execute(self, command:str) -> Answer:

        if (cursor:=self.cursor()):
            cursor.execute(command)
            self.connection.commit()
            cursor.close()
            return Answer(True)
        
        else:
            return self.logret(-3)

    #asdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjkl
    #asdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjkl
    #asdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjkl

    def check_datatypes(self, data:list, types:list) -> bool:
        if len(data) != len(types):
            return False
        check = True
        for x in zip(*[data, types]):
            if x[1] == 'int':
                if not isinstance(x[0], int):
                    check = False
                    break
            elif x[1] == 'tinytext':
                if not len(str(x[0]).encode()) < 256:
                    check = False
                    break
            elif x[1] == 'tinyint':
                if not isinstance(x[0], int) or not abs(x[0]) < 128 :
                    check = False
                    break
            elif x[1] == 'smallint':
                if not isinstance(x[0], int) or not abs(x[0]) < 32768:
                    check = False
                    break
            elif x[1] == 'mediumint':
                if not isinstance(x[0], int) or not abs(x[0]) < 8388608:
                    check = False
                    break
            elif x[1] == 'text':
                if not len(str(x[0]).encode()) < 65535:
                    check = False
                    break
            elif x[1] == 'varchar64':
                if not len(str(x[0]).encode()) < 65:
                    check = False
                    break
            elif x[1] == 'date':
                if not len(str(x[0]).encode()) == 10 and not str(x[4])+str(x[7]) == '--':
                    check = False
                    break
        return check

    # user connected functions

    def check_mail(self, mail:str) -> Answer:
        data = self.sql_conf.check_mail
        if self.check_datatypes([mail], data.take):
            return Answer(len(self.select(data.question.format(mail = mail)).getList())>0)
        return self.logret(-8)

    def check_password(self, password:str) -> Answer:
        data = self.sql_conf.check_password
        if self.check_datatypes([password], data.take):
            return Answer(len(self.select(data.question.format(password = password)).getList())>0)
        return self.logret(-8)

    def find_user(self, user_id:int) -> Answer:
        data = self.sql_conf.find_user
        if self.check_datatypes([user_id], data.take):
            return self.select(data.question.format(user_id = user_id))
        return self.logret(-8)

    def get_all_users(self) -> Answer:
        return self.select(self.sql_conf.get_all_users.question)

    def create_new_user(self, username, mail, password) -> Answer:
        data = self.sql_conf.create_new_user
        if self.check_datatypes([username, mail, password],data.take):
            return self.execute(data.question.format(username = username, mail = mail, password = password))
        return self.logret(-8)
    
    def login_user(self, mail, password) -> Answer:
        data = self.sql_conf.login_user
        if self.check_datatypes([mail,password],data.take):
            return self.select(data.question.format(mail = mail, password = password))
        return self.logret(-8)

    def last_user_created(self) -> Answer:
        return self.select(self.sql_conf.last_user_created.question)

    def update_user(self, user_id, username, mail, password) -> Answer:
        data = self.sql_conf.update_user
        if self.check_datatypes([user_id, username, mail, password],data.take):
            return self.execute(data.question.format(username = username, mail = mail, password = password, user_id = user_id))
        return self.logret(-8)

    def delete_user(self, user_id) -> Answer:
        data = self.sql_conf.delete_user
        if self.check_datatypes([user_id],data.take):
            return self.execute(data.question.format(user_id = user_id))
        return self.logret(-8)

    def get_penalty(self, user_id) -> Answer:
        data = self.sql_conf.get_penalty
        if self.check_datatypes([user_id],data.take):
            return self.select(data.question.format(user_id = user_id))
        return self.logret(-8)

    def update_penalty(self, user_id, penalty) -> Answer:
        data = self.sql_conf.update_penalty
        if self.check_datatypes([user_id, penalty], data.take):
            return self.execute(data.question.format(user_id = user_id, penalty = penalty))
        return self.logret(-8)

    # movie conected functions
        
    def find_movie(self, movie_id:int) -> Answer:
        data = self.sql_conf.find_movie
        if self.check_datatypes([movie_id,], data.take):
            return self.select(data.question.format(movie_id = movie_id))
        return self.logret(-8, notes = f'{movie_id} with {data.take}')

    def find_last_movie(self, amount:int) -> Answer:
        data = self.sql_conf.find_last_movie
        if self.check_datatypes([amount], data.take):
            return self.select(data.question.format(amount = amount))
        return self.logret(-8)

    def get_all_movies(self) -> Answer:
        return self.select(self.sql_conf.get_all_movies.question)

    def create_new_movie(self, title:str, age:int, director:str, production:int, stock:int, description:str) -> Answer:
        data = self.sql_conf.create_new_movie
        if self.check_datatypes([title, age, director, production, stock, description], data.take):
            return self.execute(data.question.format(title = title, age = age, director = director, production = production, stock = stock, description = description))
        return self.logret(-8)

    def last_movie_created(self) -> Answer:
        return self.select(self.sql_conf.last_movie_created.question)

    def update_movie(self, movie_id:int, title:str, age:int, director:str, production:int, stock:int, description:str) -> Answer:
        data = self.sql_conf.update_movie
        if self.check_datatypes([movie_id, title, age, director, production, stock, description], data.take):
            return self.execute(data.question.format(movie_id = movie_id, title = title, age = age, director = director, production = production, stock = stock, description = description))
        return self.logret(-8)

    def delete_movie(self, movie_id:int) -> Answer:
        data = self.sql_conf.delete_movie
        if self.check_datatypes([movie_id], data.take):
            return self.execute(data.question.format(movie_id = movie_id))
        return self.logret(-8)

    # tag connected functions

    def get_user_tags(self, user_id:int) -> Answer:
        data = self.sql_conf.get_user_tags
        if self.check_datatypes([user_id], data.take):
            return self.select(data.question.format(user_id = user_id))
        return self.logret(-8)
    
    def get_all_user_tags(self) -> Answer:
        return self.select(self.sql_conf.get_all_user_tags.question)

    def get_movie_tags(self, movie_id:int) -> Answer:
        data = self.sql_conf.get_movie_tags
        if self.check_datatypes([movie_id], data.take):
            return self.select(data.question.format(movie_id = movie_id))
        return self.logret(-8)
    
    def get_all_movie_tags(self) -> Answer:
        return self.select(self.sql_conf.get_all_movie_tags.question)

    def get_all_tags(self) -> Answer:
        return self.select(self.sql_conf.get_all_tags.question)

    def set_user_tag(self, user_id:int, tag_id:int) -> Answer:
        data = self.sql_conf.set_user_tag
        if self.check_datatypes([user_id, tag_id], data.take):
            return self.execute(data.question.format(user_id = user_id, tag_id = tag_id))
        return self.logret(-8)

    def delete_user_tag(self, user_id:int, tag_id:int) -> Answer:
        data = self.sql_conf.delete_user_tag
        if self.check_datatypes([user_id, tag_id], data.take):
            return self.execute(data.question.format(user_id = user_id, tag_id = tag_id))
        return self.logret(-8)

    def set_movie_tag(self, movie_id:int, tag_id:int) -> Answer:
        data = self.sql_conf.set_movie_tag
        if self.check_datatypes([movie_id, tag_id], data.take):
            return self.execute(data.question.format(movie_id = movie_id, tag_id = tag_id))
        return self.logret(-8)

    def delete_movie_tag(self, movie_id:int, tag_id:int) -> Answer:
        data = self.sql_conf.delete_movie_tag
        if self.check_datatypes([movie_id, tag_id], data.take):
            return self.execute(data.question.format(movie_id = movie_id, tag_id = tag_id))
        return self.logret(-8)

    def create_new_tag(self, name:str, description:str) -> Answer:
        data = self.sql_conf.create_new_tag
        if self.check_datatypes([name, description], data.take):
            return self.execute(data.question.format(name = name, description = description))
        return self.logret(-8)

    def delete_tag(self, tag_id:int) -> Answer:
        data = self.sql_conf.delete_tag
        if self.check_datatypes([tag_id], data.take):
            return self.execute(data.question.format(tag_id = tag_id))
        return self.logret(-8)

    def update_tag(self, tag_id:int, name:str, description:str) -> Answer:
        data = self.sql_conf.update_tag
        if self.check_datatypes([tag_id, name, description], data.take):
            return self.execute(data.question.format(tag_id = tag_id, name = name, description = description))
        return self.logret(-8)

    # rent connected functions

    def get_all_user_rents(self, user_id:int) -> Answer:
        data = self.sql_conf.get_all_user_rents
        if self.check_datatypes([user_id], data.take):
            return self.select(data.question.format(user_id = user_id))
        return self.logret(-8)

    def get_all_movie_rents(self, movie_id:int) -> Answer:
        data = self.sql_conf.get_all_movie_rents
        if self.check_datatypes([movie_id], data.take):
            return self.select(data.question.format(movie_id = movie_id))
        return self.logret(-8)
    
    def get_all_outdated(self, date:str) -> Answer:
        data = self.sql_conf.get_all_outdated
        if self.check_datatypes([date], data.take):
            return self.select(data.question.format(date = date))
        return self.logret(-8)
    
    def get_all_not_returned(self) -> Answer:
        return self.select(self.sql_conf.get_all_not_returned.question)
    
    def update_rent(self, movie_id:int, user_id:int, rent:str, return_date:str, real_return:str, rent_id:int) -> Answer:
        data = self.sql_conf.update_rent
        if self.check_datatypes([movie_id, user_id, rent, return_date, real_return, rent_id], data.take):
            return self.execute(data.question.format(movie_id = movie_id, user_id = user_id, rent = rent, return_date = return_date, real_return = real_return, rent_id = rent_id))
        return self.logret(-8)
    
    def return_rent(self, rent_id:int, date:str) -> Answer:
        data = self.sql_conf.return_rent
        if self.check_datatypes([rent_id, date], data.take):
            return self.execute(data.question.format(real_return = date, rent_id = rent_id))
        return self.logret(-8)
    
    def create_new_rent(self, movie_id:int, user_id:int, rent:str, return_date:str) -> Answer:
        data = self.sql_conf.create_new_rent
        if self.check_datatypes([movie_id, user_id, rent, return_date], data.take):
            return self.execute(data.question.format(movie_id = movie_id, user_id = user_id, rent = rent, return_date = return_date,))
        return self.logret(-8)
    
    def delete_rent(self, rent_id:int) -> Answer:
        data = self.sql_conf.delete_rent
        if self.check_datatypes([rent_id], data.take):
            return self.execute(data.question.format(rent_id = rent_id))
        return self.logret(-8)
    
    def get_all_before(self, date:str) -> Answer:
        data = self.sql_conf.get_all_before
        if self.check_datatypes([date], data.take):
            return self.select(data.question.format(date = date))
        return self.logret(-8)
    
    def get_all_after(self, date:str) -> Answer:
        data = self.sql_conf.get_all_after
        if self.check_datatypes([date], data.take):
            return self.select(data.question.format(date = date))
        return self.logret(-8)
    
    def get_all_user_rented_returned(self, user_id:int) -> Answer:
        data = self.sql_conf.get_all_user_rented_returned
        if self.check_datatypes([user_id], data.take):
            return self.select(data.question.format(user_id = user_id))
        return self.logret(-8)
    
    def get_all_user_rented_not_returned(self, user_id:int) -> Answer:
        data = self.sql_conf.get_all_user_rented_not_returned
        if self.check_datatypes([user_id], data.take):
            return self.select(data.question.format(user_id = user_id))
        return self.logret(-8)
    
    def get_all_user_outdated(self, user_id:int, date:str) -> Answer:
        data = self.sql_conf.get_all_user_outdated
        if self.check_datatypes([user_id, date], data.take):
            return self.select(data.question.format(user_id = user_id, date = date))
        return self.logret(-8)
    
    def get_user_movie_rent(self, user_id:int, movie_id:int) -> Answer:
        data = self.sql_conf.get_user_movie_rent
        if self.check_datatypes([user_id, movie_id], data.take):
            return self.select(data.question.format(user_id = user_id, movie_id = movie_id))
        return self.logret(-8)

    # unspecified

    def check_userdata(self, typ:str, value:str) -> Answer:
        data = self.sql_conf.check_userdata
        if not self.check_datatypes([typ, value], data.take):
            return self.logret(-8)
        if not typ in self.sql_conf.user.columns_names:
            return self.logret(-5)
        return self.select(data.question.format(type = typ, value = value))
        
    
    #asdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjkl
    #asdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjkl
    #asdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjklasdfghjkl

    #deprived function for trimming lists
    #def distable(self, data:list) -> list:
        #if len(data) == 1:
            #if len(data[0]) == 1:
                #return data[0][0]
            #else:
                #return data[0]
        #return [i[0] if len(i) == 1 else i for i in data]

    #deprived function for getting id from querry
    #def return_id(self, data:list) -> list:
        #return [i[0] for i in data]


    #regex check for valid email
    def mail_check(self, mail:str) -> bool:
        return bool(re.compile(".+@.+\..+").search(mail))


    #regex check for SQL injection
    def protection(self, question:str) -> str:
        return question[:- answer.span()[0]] if bool(answer:=re.compile(r".* or .*", re.I).search(question)) else question


    #regex check for valid password
    def password_check(self, password:str) -> bool:
        return bool(re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$').search(password))
        
    #checks if data is valid
    def userdata_check(self, typ:str, value:str) -> Answer:

        self.__log__(-1016, notes = f'on {typ} with {value}')
        return Answer(len(self.check_userdata(typ, value).getList()) == 1)
    
    def user_exists(self, user_id) -> bool:

        self.__log__(-1022, notes = f'user_id -> {user_id}')
        a = self.find_user(user_id)
        if a.isUsefull():
            if len(a.getList())>0:
                return True
        return False
        
    def movie_exists(self, movie_id:int) -> bool:

        self.__log__(-1022, notes = f'movie_id -> {movie_id}')
        a = self.find_movie(movie_id)
        if a.isUsefull():
            if len(a.getList())>0:
                q = self.get_movie_tags(int(a.getList()[0]))
                if q.isUsefull():
                    if self.tag_name(q.getList()[0]) == 'deleted':
                        return False
                return True
        return False

    #checks if user is active
    def inactivity_check(self, user_id:int) -> bool:
        
        self.__log__(-1017, notes = f'user_id = {user_id}')
        if not self.user_exists(user_id):
            self.__log__(-1005, notes = f'user_id -> {user_id}')
            return False
        answer = self.get_user_tags(user_id).getList()
        if not self.get_tag_id('inactive') in answer:
            self.__log__(-1023, notes = f'user_id -> {user_id}')
            return True
        self.__log__(-1004, notes = f'user_id -> {user_id}')
        return False

    def ban_check(self, user_id:int) -> bool:
        
        self.__log__(-1017, notes = f'user_id = {user_id}')
        if not self.user_exists(user_id):
            self.__log__(-1005, notes = f'user_id -> {user_id}')
            return False
        answer = self.get_user_tags(user_id).getList()
        if not self.get_tag_id('banned') in answer:
            self.__log__(-1023, notes = f'user_id -> {user_id}')
            return False
        self.__log__(-1004, notes = f'user_id -> {user_id}')
        return True
    
    def get_ban_id(self) -> int:
        return list(zip(*self.get_all_tags().getList()))[1].index('banned')+1
    
    def get_tag_id(self, tagname) -> int:
        try:
            return list(zip(*self.get_all_tags().getList()))[1].index(tagname)+1
        except:
            return -1

    def user_ban_status(self, user_id:int, ban_id=-1) -> Answer:

        if not ban_id >= 0:
            ban_id = self.get_ban_id()
        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')
        user_tags = self.get_user_tags(user_id).getList()
        self.__log__(-1012, notes = f'user_id -> {user_id}')
        if not ban_id in user_tags:
            return Answer(False)
        return Answer(True)
    
    def user_deactivate(self, user_id:int) -> Answer:

        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')

        question = self.inactivity_check(user_id)

        if not question:
            return self.logret(-1004)

        question = self.set_user_tag(user_id, self.get_tag_id('inactivity'))

        if question.isError():
            return question
        
        if question.getBool():
            return self.logret(-1028, notes = f'user_id -> {user_id}')
        return self.logret(-1029, notes = f'user_id -> {user_id}')

    def user_ban(self, user_id:int) -> Answer:

        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')

        question = self.user_ban_status(user_id)

        if question.isError():
            return question
        
        if question.getBool():
            return self.logret(-1006, notes = f'user_id -> {user_id}')

        question = self.set_user_tag(user_id, self.get_ban_id())

        if question.isError():
            return question
        
        if question.getBool():
            return self.logret(-1007, notes = f'user_id -> {user_id}')
        return self.logret(-1024, notes = f'user_id -> {user_id}')
    
    #DO NOT USE FOR NOW
    def user_activate(self, user_id:int) -> Answer:

        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')

        question = self.inactivity_check(user_id)

        if not question:
            return self.logret(-1004)

        question = self.delete_user_tag(user_id, self.get_tag_id('inactivity'))

        if question.isError():
            return question
        
        if question.getBool():
            return self.logret(-1028, notes = f'user_id -> {user_id}')
        return self.logret(-1029, notes = f'user_id -> {user_id}')
        
    def user_unban(self, user_id:int) -> Answer:
        
        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')

        question = self.user_ban_status(user_id)

        if question.isError():
            return question
        
        if not question.getBool():
            return self.logret(-1006, notes = f'user_id -> {user_id}')

        question = self.delete_user_tag(user_id, self.get_ban_id())

        if question.isError():
            return question
        
        if question.getBool():
            return self.logret(-1009, notes = f'user_id -> {user_id}')
        return self.logret(-1025, notes = f'user_id -> {user_id}')
    
    #creates new user to database
    def new_user(self, username:str, mail:str, password:str, admin=False) -> Answer:
        
        username = self.protection(username)
        mail = self.protection(mail)
        password = self.protection(password)

        if not self.mail_check(mail):
            return self.logret(-1001)

        if not self.password_check(password):
            return self.logret(-1001)

        #q = self.check_userdata('username',username)
        #if q.isError():
            #return self.logret(-1015)
        #if not len(q.getList()) > 0:
            #return self.logret(-1003, notes = f'simmilar username found -> {username}')

        q = self.check_mail(mail)
        if q.isError():
            return self.logret(-1015)
        if len(q.getList()) > 0:
            return self.logret(-1001, notes = f'simmilar mail found -> {mail}')

        if not self.create_new_user(username, mail, password):
            self.logret(-1015, notes = f'username -> {username} , mail -> {mail} , password -> {password}')
        
        user_id = self.last_user_created().getId()

        if admin:
            admin_tag = self.get_tag_id('admin')
            q = self.set_user_tag(user_id, admin_tag)
            if not q.isUsefull():
                self.__log__(-3001, notes = f'tag_id -> {admin_tag}')
            
        self.__log__(-1018, notes = f'username -> {username} , mail -> {mail} , password -> {password}')
        return self.find_user(self.last_user_created().getId())

    #checks if data provided is valid and user can be logged in
    #    returns data of user
    def user_login(self, mail:str, password:str) -> Answer:
        
        mail = self.protection(mail)
        password = self.protection(password)

        if not self.mail_check(mail):
            return self.logret(-1001)

        if not self.password_check(password):
            return self.logret(-1001)

        user_id = self.login_user(mail, password)

        if user_id.isError():
            return self.logret(-1026, notes = f'mail -> {mail} password -> {password}')
        
        if len(user_id.getList()) == 0:
            return self.logret(-1002, notes = f'mail -> {mail} password -> {password}')
        
        user_id = user_id.getId()

        if self.user_ban_status(user_id).getBool():
            return self.logret(-1011)
        
        question = self.inactivity_check(user_id)

        if not question:
            return self.logret(-1004)
        
        self.__log__(-1019, notes = f'user id -> {user_id}')
        return self.find_user(user_id)
            
    #changes data of a user
    def userdata_change(self, user_id:int, username:str, mail:str, password:str, tags=[]) -> Answer:

        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')

        username = self.protection(username)
        mail = self.protection(mail)
        password = self.protection(password)

        if not self.mail_check(mail):
            return self.logret(-1001)

        if not self.password_check(password):
            return self.logret(-1001)

        #q = self.check_userdata('username',username)
        #if q.isError():
            #return self.logret(-1015)
        #if len(q.getList()) > 0:
            #return self.logret(-1003, notes = f'simmilar username found -> {username}')

        q = self.check_userdata('mail',mail)
        if q.isError():
            return self.logret(-1015)
        if len(q.getList()) > 0:
            return self.logret(-1001, notes = f'simmilar mail found -> {mail}')

        question = self.inactivity_check(user_id)

        if not question:
            return self.logret(-1004)

        if password == '':
            password = self.find_user(user_id).getList()[3]

        self.update_user(user_id, username, mail, password)
        
        if len(tags) > 0:
            q = self.get_all_tags()
            if not q.isUsefull():
                self.__log__(-2001)
            else:
                user_tags = self.get_user_tags(user_id)
                if not user_tags.isUsefull():
                    self.__log__(-2001)
                else:
                    user_tags  = user_tags .getList()
                    for x in tags.copy():
                        if not x in q:
                            self.__log__(-3000, notes = f'tag_id -> {x}')
                            if x in user_tags:
                                p = self.set_user_tag(user_id, x)
                                if not p.isUsefull():
                                    self.__log__(-3001, notes = f'tag_id -> {x}')

                    for x in user_tags:
                        if not x in tags:
                            p = self.delete_user_tag(user_id, x)
                            if not p.isUsefull():
                                self.__log__(-3001, notes = f'tag_id -> {x}')

        self.__log__(-1020, notes=f"new user data -> username:{username} mail:{mail} password:{password} :: with an id -> {user_id}")
        return Answer(True)

    #deletes user, by setting his activity status to False
    def user_delete(self, user_id:int) -> Answer:
        
        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')
        
        q = self.get_all_user_rented_not_returned(user_id)
        if q.isError():
            return self.logret(-10001)
        if len(q.getList()) == 0:
            q2 = self.user_finder(user_id)
            q = self.update_user(user_id, q2.getList()[1],'','')
            if q.isError():
                return self.logret(-1030, notes = f'user_id -> {user_id}')
            
            q = self.user_deactivate(user_id)
            return self.logret(-1021, notes = f'user_id -> {user_id}')
        return self.logret(-1030, notes = f'user_id -> {user_id}')
    
    def stock_add(self, movie_id, amount) -> Answer:

        if not self.movie_exists(movie_id):
            return self.logret(-2004, notes = f'movie_id -> {movie_id}')
        
        q = self.movie_finder(movie_id).getList()
        return self.movie_change_add_tags(movie_id, q[1], [], q[2], q[3], q[4], q[5]+amount, q[6])
    
    def stock_sub(self, movie_id, amount) -> Answer:

        if not self.movie_exists(movie_id):
            return self.logret(-2004, notes = f'movie_id -> {movie_id}')
        
        q = self.movie_finder(movie_id).getList()
        return self.movie_change_add_tags(movie_id, q[1], [], q[2], q[3], q[4], q[5]-amount, q[6])

    #gets movies rented by the user
    def user_rent_history(self, user_id:int) -> Answer:
        
        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')
        
        q = self.get_all_user_rents(user_id)
        if not q.isUsefull():
            return self.logret(-4000)
        return q
    
    def user_actual_rent(self, user_id:int) -> Answer:
        
        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')
        
        q = self.get_all_user_rented_not_returned(user_id)
        if not q.isUsefull():
            return self.logret(-4000)
        return q
    
    def user_have_return(self, user_id:int, date:str) -> Answer:
        
        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')
        
        q = self.get_all_user_outdated(user_id, date)
        if not q.isUsefull():
            return self.logret(-4000)
        return q
    
    def user_old_rent(self, user_id:int) -> Answer:
        
        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')
        
        q = self.get_all_user_rented_returned(user_id)
        if not q.isUsefull():
            return self.logret(-4000)
        return q

    def movie_rented(self, movie_id:int) -> Answer:

        if not self.movie_exists(movie_id):
            return self.logret(-2004, notes = f'movie_id -> {movie_id}')
        
        q = self.get_all_movie_rents(movie_id)
        if not q.isUsefull():
            return self.logret(-4001)
        return q
    
    def rents_user_outdated(self, user_id:int) -> Answer:
        
        today = datef.today().strftime('%Y-%m-%d')
        q = self.user_rented(user_id)
        if q.isError():
            return q.getError()
        
        q2 = self.get_all_outdated(today)    
        if q2.isError():
            return q2.getError()

        answer = []

        for x in q:
            if x in q2:
                answer.append(x)
        
        return Answer(answer)
    
    def rents_movie_outdated(self, movie_id) -> Answer:
        
        today = datef.today().strftime('%Y-%m-%d')
        q = self.movie_rented(movie_id)
        if q.isError():
            return q.getError()
        
        q2 = self.get_all_outdated(today)    
        if q2.isError():
            return q2.getError()

        answer = []

        for x in q:
            if x in q2:
                answer.append(x)
        
        return Answer(answer)
    
    def rents_all_outdated(self) -> Answer:

        today = datef.today().strftime('%Y-%m-%d')
        q = self.get_all_outdated(today)    
        if not q.isUsefull():
            return self.logret(-4002)
        return q
    
    def rents_not_returned(self) -> Answer:

        q = self.get_all_not_returned()
        if not q.isUsefull():
            return self.logret(-4002)
        return q
    
    def rent_update(self, rent_id, movie_id, user_id, rent, return_date, real_return) -> Answer:
        
        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')

        if not self.movie_exists(movie_id):
            return self.logret(-2004, notes = f'movie_id -> {movie_id}')

        q = self.update_rent(movie_id, user_id, rent, return_date, real_return, rent_id)
        if not q.isUsefull():
            return self.logret(-4003)
        return q
    
    def rent_return(self, rent_id, date) -> Answer:

        q = self.return_rent(rent_id, date)
        if not q.isUsefull():
            return self.logret(-4006)
        return q
    
    def rent(self, movie_id, user_id, rent, return_date) -> Answer:
        
        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')

        if not self.movie_exists(movie_id):
            return self.logret(-2004, notes = f'movie_id -> {movie_id}')

        q = self.create_new_rent(movie_id, user_id, rent, return_date)
        if not q.isUsefull():
            return self.logret(-4004)
        q = self.stock_sub(movie_id, 1)
        if not q.isUsefull():
            return self.logret(-2005)
        return q
    
    def unrent(self, rent_id:int, movie_id:int, date:str) -> Answer:

        q = self.return_rent(rent_id, date)
        if not q.isUsefull():
            return self.logret(-4005)
        q = self.stock_add(movie_id, 1)
        if not q.isUsefull():
            return self.logret(-2005)
        return q

    def rented_before(self, date) -> Answer:

        q = self.get_all_before(date)
        if not q.isUsefull():
            return self.logret(-4005)
        return q
    
    def rented_after(self, date) -> Answer:

        q = self.get_all_after(date)
        if not q.isUsefull():
            return self.logret(-4005)
        return q

    #Adds a movie to database
    def movie_add(self, title:str, age:int, director:str, production:int, stock:int, tags:list[int], description="") -> Answer:
        
        title = self.protection(title)
        director = self.protection(director)
        description = self.protection(description)

        q = self.get_all_tags()
        if not q.isUsefull():
            self.__log__(-2001)
        q = q.getList()
        for x in tags.copy():
            if not x in tags:
                self.__log__(-3000, notes = f'tag_id -> {x}')
                tags.remove(tags.index(x))

        if not int(production) > 1995:
            return self.logret(-2000,notes=f"year provided -> {production}")
        q = self.create_new_movie(title, age, director, production, stock, description)
        if not q.isUsefull():
            return self.logret(-2002, notes=f"movie data -> title:{title} age:{age} director:{director} production_year:{production} stock:{stock} description:{description}")
        movie = self.last_movie_created()
        if not movie.isUsefull():
            return self.logret(-10001, notes=f"movie data -> title:{title} age:{age} director:{director} production_year:{production} stock:{stock} description:{description}")
        movie_id = movie.getId()
        for x in tags:
            q = self.set_movie_tag(movie_id, x)
            if not q.isUsefull():
                self.__log__(-3001, notes = f'tag_id -> {x}')
        
        self.__log__(-2003, notes=f"movie data -> title:{title} age:{age} director:{director} production_year:{production} stock:{stock} description:{description}")
        return movie_id

    #Searches database for a movie by given criterion
    #
    #   !!!TO BE DONE!!!
    #
    def movies_find_strict(self, tags=[], name='', age_min=0, age_max=99, director='', production_min=0, production_max=9999, onstock=False) -> Answer:
        
        q = self.get_all_movies()
        if not q.isUsefull():
            return self.logret(-10001)
        q = q.getList()
        for x in tags.copy():
            gt = self.get_tag_id(x)
            if gt == -1:
                del tags[tags.index(x)]
            else:
                tags[tags.index(x)] = gt

        for x in q.copy():
            if len(q) == 0:
                break
            qq = self.get_movie_tags(x[0])
            if not qq.isUsefull():
                self.__log__(-3000, notes = f'tag_id -> {x}')
            if (len(tags) > 0 and not set(qq.getList()) & set(tags)) or x[1].find(name) == -1 or not x[2] >= age_min or not x[2] <= age_max or x[3].find(director) == -1 or not x[4] >= production_min or not x[4] <= production_max or (onstock and x[5] == 0):
                del q[q.index(x)]
                continue
            qqq = self.find_movie(x[0])
            if not qqq.isUsefull():
                self.__log__(-10001)
                del q[q.index(x)]
            else:
                q[q.index(x)] = qqq
        
        return Answer(q)
    
    def movies_find_lazy(self, tags=[], name='', age_min=0, age_max=99, director='', production_min=0, production_max=9999, onstock=False) -> Answer:
        
        q = self.get_all_movies()
        if not q.isUsefull():
            return self.logret(-10001)
        q = q.getList()
        for x in tags.copy():
            gt = self.get_tag_id(x)
            if gt == -1:
                del tags[tags.index(x)]
            else:
                tags[tags.index(x)] = gt

        for x in q.copy():
            if len(q) == 0:
                break
            qq = self.get_movie_tags(x[0])
            if not qq.isUsefull():
                self.__log__(-3000, notes = f'tag_id -> {x}')
            if (len(tags) > 0 and not set(qq.getList()) & set(tags)) and x[1].find(name) == -1 and not x[2] >= age_min and not x[2] <= age_max and x[3].find(director) == -1 and not x[4] >= production_min and not x[4] <= production_max and (onstock and x[5] == 0):
                del q[q.index(x)]
                continue
            qqq = self.find_movie(x[0])
            if not qqq.isUsefull():
                self.__log__(-10001)
                del q[q.index(x)]
            else:
                q[q.index(x)] = qqq
        return Answer(q)

    #Searches for a movie by id
    def movie_finder(self, movie_id:int) -> Answer:
        
        if not self.movie_exists(movie_id):
            return self.logret(-2004, notes = f'movie_id -> {movie_id}')
        return self.find_movie(movie_id)
    
    def movie_tags(self, movie_id:int) -> Answer:

        if not self.movie_exists(movie_id):
            return self.logret(-2004, notes = f'movie_id -> {movie_id}')
        question = self.get_movie_tags(movie_id)
        if not question.isUsefull():
            return question
        a = []
        c = self.get_all_tags().getList()
        b = list(zip(*c))[0]
        
        for x in question.getList():
            if x in b:
                a.append(c[b.index(x)])
        return Answer(a)

    #Searches for a user by id
    def user_finder(self, user_id:int) -> Answer:
        
        if not self.user_exists(user_id):
            return self.logret(-1004, notes = f'user_id -> {user_id}')
        return self.find_user(user_id)

    #Changes data of a movie
    #
    #   TO BE UPDATED
    #
    def movie_change(self, movie_id:int, title:str, tags:list[int], age:int, director:str, production:int, stock:int, description:str) -> Answer:
        
        title = self.protection(title)
        director = self.protection(director)
        description = self.protection(description)

        q = self.get_all_tags()
        if not q.isUsefull():
            self.__log__(-2001)
        else:
            movie_tags = self.get_movie_tags(movie_id)
            if not movie_tags.isUsefull():
                self.__log__(-2001)
            else:
                movie_tags = movie_tags.getList()
                for x in tags.copy():
                    if not x in q:
                        self.__log__(-3000, notes = f'tag_id -> {x}')
                        if x in movie_tags:
                            p = self.set_movie_tag(movie_id, x)
                            if not p.isUsefull():
                                self.__log__(-3001, notes = f'tag_id -> {x}')

                for x in movie_tags:
                    if not x in tags:
                        p = self.delete_movie_tag(movie_id, x)
                        if not p.isUsefull():
                            self.__log__(-3001, notes = f'tag_id -> {x}')

        return self.update_movie(movie_id, title, age, director, production, stock, description=description)
    
    def movie_change_add_tags(self, movie_id:int, title:str, tags:list[int], age:int, director:str, production:int, stock:int, description:str) -> Answer:
        
        title = self.protection(title)
        director = self.protection(director)
        description = self.protection(description)

        q = self.get_all_tags()
        if not q.isUsefull():
            self.__log__(-2001)
        else:
            movie_tags = self.get_movie_tags(movie_id)
            if not movie_tags.isUsefull():
                self.__log__(-2001)
            else:
                movie_tags = movie_tags.getList()
                for x in tags.copy():
                    if not x in q:
                        self.__log__(-3000, notes = f'tag_id -> {x}')
                        continue
                    if not x in movie_tags:
                        p = self.set_movie_tag(movie_id, x)
                        if not p.isUsefull():
                            self.__log__(-3001, notes = f'tag_id -> {x}')

        return self.update_movie(movie_id, title, age, director, production, stock, description=description)

    #Gets recently added movies
    def movies_recent(self, amount:int) -> Answer:
        return self.find_last_movie(amount)
    def the_best_movie(self, lim:int) -> Answer:
        return self.select(self.sql_conf.the_best.question.format(lim=lim))
    #set stock amount of movie by id to 0
    def movie_delete(self, movie_id:int) -> Answer:
        q = self.movie_finder(movie_id)
        if q.isUsefull():
            return self.movie_change(movie_id, q.getList()[1], ['deleted'], 0, '', 0, 0, '')
        return Answer(None)

    #actually, I don't know why this even exists, not used anymore!
    def all_from_all(self, table:str) -> Answer:

        return Answer(False)

        if not table in ["movie", "user", "rent", "tags"]:
            self.__log__(-8, notes=f"not good table name")
            return Answer(self.__codes__[-8])
        
        if(cursor:=self.cursor()):
            answer = self.select(cursor, f"SELECT * FROM {table}")
            cursor.close()
            return Answer(answer)

        self.__log__(-200)
        return Answer(self.__codes__[-200])
    
    #deprived
    def getStatus(self, id:int) ->Answer:

        return Answer(False)

        if(cursor:=self.cursor()):
            answer = self.select(cursor, f"Select active from user where id = {id}")
            cursor.close()
            return Answer(answer)
        else:
            self.__log__(-200)
    
    def movie_all_tags(self) -> Answer:
        q = self.get_all_movie_tags()
        if not q.isUsefull():
            return Answer(None)
        return q

    def admin(self, user_id:int) -> Answer:
        q = self.get_user_tags(user_id)
        if not q.isUsefull():
            return self.logret(-3003)
        q = q.getList()
        return Answer(self.get_tag_id('admin') in q)

    def rent_id_ideal(self, user_id, movie_id) -> Answer:

        if not self.user_exists(user_id):
            return self.logret(-1005, notes = f'user_id -> {user_id}')

        if not self.movie_exists(movie_id):
            return self.logret(-2004, notes = f'movie_id -> {movie_id}')
        
        return self.get_user_movie_rent(user_id, movie_id)
    
    def users_all(self) -> Answer:
        return self.get_all_users()

    def tag_name(self, tag_id:int) -> Answer:
        q = self.get_all_tags()
        if q.isUsefull():
            l = list(zip(*q.getList()))
            if l[1].count(tag_id) > 0:
                return Answer(l[l[1].index(tag_id)])
        return Answer(None)
    def the_best_movie(self, lim:int) -> Answer:
        return self.select(self.sql_conf.the_best.question.format(lim=lim))