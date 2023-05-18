import bottle
from bottle import url

#from codebase.modules import *
#from codebase.sitescripts import funclist as fl
from codebase.SQL.connect import SQL
from codebase.SQL.answer import Answer
from codebase.Tools.structure import Struct
from codebase.Tools.sites import Site

from abc import ABC, abstractmethod
from datetime import date, timedelta
from random import choice
from string import ascii_letters
from os import getcwd, scandir

session_opts = {
    'session.type' : 'memory',
    'session.cookie_expires' : 1200,
    'session.auto' : True
    }

class Application(bottle.Bottle):

    route_list = []
    error_list = []
    SQL_Connection: SQL
    frontD: str
    
    def __init__(self, sql:SQL,secret="", static_folder="./../front/data", template_folder="./../front/sites", front_folder="./../front", old_setup=False):
        super()
        bottle.debug(True)
        self.SQL_Connection = sql
        self.frontD = front_folder

        if len(secret)>0:
            self.setSecret(bytes(secret, 'utf-8'))
        @bottle.route("/static/<filepath:path>")
        def static(filepath):
            return bottle.static_file(filepath, root=static_folder)

        bottle.TEMPLATE_PATH = [template_folder]
        if old_setup:
            self.old_setup()
        else:
            self.setup(template_folder)


    def addroute(self, route:callable):
        self.route_list.append(route)

    def adderror(self, error:callable):
        self.error_list.append(error)

        
    def setSecret(self, secret_key):
        self.secret = secret_key

        
    def old_setup(self):
        pass

    def setup(self, path:str):
        self.sites = []
        for x in [f.path.replace('\\', '/') for f in scandir(path) if f.is_dir()]:
            if x.split('/')[-1] not in ['Filmy','.Errors']:
                self.sites.append(Create.Site(self.SQL_Connection, x, x.split('/')[-1], menubar=Create.html.standard.menubar()))

        for x in self.sites:
            self.addroute(Create.bottle.route(self, x.route, Create.function.withSite(x), x.name))

        self.errors = []
        path = path + '\\.Errors'.replace('\\', '/')
        for x in [f.path.replace('\\', '/') for f in scandir(path) if f.is_dir()]:
            self.errors.append(Create.Site(self.SQL_Connection, x, x.split('/')[-1]))

        for x in self.errors:
            self.adderror(Create.bottle.error(self, int(x.route), Create.function.withESite(x), x.name))

    def runApp(self, host="", port=8080, debug=False):
        bottle.run(host=host, port=port)
    
class Response(bottle.HTTPResponse):
    pass

class Create(ABC):

    @abstractmethod
    def Site(sql:SQL, configfile:str, name:str, *args, headers={'Content-Type': 'text/html'}, **kwargs):
        return Site(configfile, name, headers, sql, *args, **kwargs)
    
    class usefull(ABC):
        @abstractmethod
        def MergeDict(a:dict, b:dict) -> dict:
            return a | b
    class bottle(ABC):
        @abstractmethod
        def route(app:bottle.Bottle, route:str, base_function:callable, route_id:str, methods=['GET','POST'], *args, **kwargs) -> callable:
            @bottle.route(route, method=methods, name=route_id)
            def f(*args, **kwargs):
                return base_function(*args, **kwargs)
            return f
        def error(app:bottle.Bottle, error:int, base_function:callable, *args, **kwargs) -> callable:
            @bottle.error(error)
            def f(*args, **kwargs):
                return base_function(*args, **kwargs)
            return f
        
        @abstractmethod
        def dynamicRoute(app:bottle.Bottle, route:str, base_function:callable,route_id:str, methods=['GET','POST'], *args, **kwargs) -> callable:
            @app.route(route, method=methods, name=route_id)
            def f(*args, **kwargs):
                return base_function(*args, **kwargs)
            return f
        
    class function(ABC):
        @abstractmethod
        def withSite(thisSite:Site, wrapper=(lambda n, **kwg: n(**kwg)), statuscode=200) -> callable:
            return lambda : wrapper(thisSite.Answer(statuscode))
        
        @abstractmethod
        def withESite(thisSite:Site, wrapper=(lambda n, *args, **kwg: n(*args, **kwg))) -> callable:
            return lambda *args, **kwargs: wrapper(thisSite.Answer(int(thisSite.route)))
        
        @abstractmethod
        def withTemplate(template:str, wrapper=(lambda n: n()), **kwargs) -> callable:
            return lambda : wrapper(lambda **kwg : bottle.Response(body=bottle.template(template, **Create.usefull.MergeDict(kwargs, kwg)), headers = {'Content-Type': 'text/html'}, status_code = 200))

        @abstractmethod
        def withFunction(function:callable, wrapper=(lambda n: n), **kwargs) -> callable:
            return lambda : wrapper(lambda **kwg : bottle.Response(body=function(**Create.usefull.MergeDict(kwargs, kwg)), headers = {'Content-Type': 'text/html'}, status_code = 200))

        @abstractmethod
        def rawFunction(function:callable, **kwargs) -> callable:
            return lambda : function(**kwargs)

    class html(ABC):
        class base(ABC):
            @abstractmethod
            def withFunctions(head:callable,body:callable) -> str:
                a, b = head(), body()
                return f'''
                    <html>
                    <head>
                        {a}
                    </head>
                    <body>
                        {b}
                    </body>
                    </html>
                '''
            def withText(head:str, body:str) -> str:
                return f'''
                    <html>
                    <head>
                        {head}
                    </head>
                    <body>
                        {body}
                    </body>
                    </html>
                '''
        class standard(ABC):
            @abstractmethod
            def menubar():
                return "deprived"
if __name__=="__main__":
    pass
