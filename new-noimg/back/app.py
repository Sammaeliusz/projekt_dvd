import bottle
from bottle import url

from codebase.modules import *
#from codebase.sitescripts import funclist as fl
import codebase.uses as Uses
from codebase.sites import Site

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
    def __init__(self,secret="", static_folder="./../front/data", template_folder="./../front/sites", front_folder="./../front", old_setup=False):
        super()
        bottle.debug(True)
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
    def setSecret(self, secret_key):
        self.secret = secret_key
    def old_setup(self):
        self.addroute(Create.bottle.route(self, '/',               Create.function.withTemplate("index.php",          menubar=Create.html.standard.menubar()), "index"))
        self.addroute(Create.bottle.route(self, '/panel',          Create.function.withTemplate("panel.php",          wrapper=fl['panel'], menubar=Create.html.standard.menubar()), 'panel'))
        self.addroute(Create.bottle.route(self, '/userclick',      Create.function.rawFunction(fl['userclick']), 'userclick'))
        self.addroute(Create.bottle.route(self, '/logowanie',      Create.function.withTemplate("logowanie.php",      wrapper=fl['login'], menubar=Create.html.standard.menubar()), "login"))
        self.addroute(Create.bottle.route(self, '/zmiana',         Create.function.withTemplate("zmiana.php",         wrapper=fl['zmiana'], menubar=Create.html.standard.menubar()), "zmiana"))
        self.addroute(Create.bottle.route(self, '/rejestracja',    Create.function.withTemplate("rejestracja.php",    wrapper=fl['register'], menubar=Create.html.standard.menubar()), "register"))
        self.addroute(Create.bottle.route(self, '/gatunek',        Create.function.withTemplate("kategorie.php",      menubar=Create.html.standard.menubar()), "gatunek"))
        self.addroute(Create.bottle.route(self, '/rezyser',        Create.function.withTemplate("rezyser.php",        menubar=Create.html.standard.menubar()), "rezyser"))
        self.addroute(Create.bottle.route(self, '/rok',            Create.function.withTemplate("rok.php",            menubar=Create.html.standard.menubar()), "rok"))
        self.addroute(Create.bottle.route(self, '/zbiory',         Create.function.withTemplate("zbiory.php",         wrapper=fl['zbiory'], menubar=Create.html.standard.menubar()), "zbiory"))

    def setup(self, path:str):
        self.sites = []
        for x in [f.path.replace('\\', '/') for f in scandir(path) if f.is_dir()]:
            if x.split('/')[-1] not in ['Filmy']:
                self.sites.append(Create.Site(x, x.split('/')[-1], menubar=Create.html.standard.menubar()))

        for x in self.sites:
            self.addroute(Create.bottle.route(self, x.route, Create.function.withSite(x), x.name))

    def runApp(self, host="", port=8080, debug=False):
        bottle.run(host=host, port=port)
    
class Response(bottle.HTTPResponse):
    pass

class Create(ABC):

    @abstractmethod
    def Site(configfile:str, name:str, *args, headers={'Content-Type': 'text/html'}, **kwargs):
        return Site(configfile, name, headers, *args, **kwargs)
    
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
        
        @abstractmethod
        def dynamicRoute(app:bottle.Bottle, route:str, base_function:callable,route_id:str, methods=['GET','POST'], *args, **kwargs) -> callable:
            @app.route(route, method=methods, name=route_id)
            def f(*args, **kwargs):
                return base_function(*args, **kwargs)
            return f
        
    class function(ABC):
        @abstractmethod
        def withSite(thisSite:Site, wrapper=(lambda n: n()), statuscode=200) -> callable:
            return lambda : wrapper(thisSite.Answer(statuscode))
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
                with open("./../front/standard/menubar.txt", 'rb') as f:
                    return f.read().decode("utf-8")
if __name__=="__main__":
    app = Application(template_folder='/projekt/front/templates/', static_folder='/projekt/front/data/')
    app.setSecret(b'dgf;hpo4[]t,drgtp[e45.g')

    #''.join(choice(ascii_letters) for i in range(32))
    app.addroute(Create.bottle.route(app, '/',               Create.function.withTemplate("index.php",          wrapper=index, menubar=Create.html.standard.menubar()), "index"))
    app.addroute(Create.bottle.route(app, '/panel',          Create.function.withTemplate("panel.php",          wrapper=panel, menubar=Create.html.standard.menubar()), 'panel'))
    app.addroute(Create.bottle.route(app, '/userclick',      Create.function.withFunction(userclick), 'userclick'))
    app.addroute(Create.bottle.route(app, '/logowanie',      Create.function.withTemplate("logowanie.php",      wrapper=login, menubar=Create.html.standard.menubar()), "login"))
    app.addroute(Create.bottle.route(app, '/zmiana',         Create.function.withTemplate("zmiana.php",         wrapper=zmiana, menubar=Create.html.standard.menubar()), "zmiana"))
    app.addroute(Create.bottle.route(app, '/rejestracja',    Create.function.withTemplate("rejestracja.php",    wrapper=register, menubar=Create.html.standard.menubar()), "register"))
    app.addroute(Create.bottle.route(app, '/gatunek',        Create.function.withTemplate("kategorie.php",      wrapper=gatunek, menubar=Create.html.standard.menubar()), "gatunek"))
    app.addroute(Create.bottle.route(app, '/rezyser',        Create.function.withTemplate("rezyser.php",        wrapper=rezyser, menubar=Create.html.standard.menubar()), "rezyser"))
    app.addroute(Create.bottle.route(app, '/rok',            Create.function.withTemplate("rok.php",            wrapper=rok, menubar=Create.html.standard.menubar()), "rok"))
    app.addroute(Create.bottle.route(app, '/zbiory',         Create.function.withTemplate("zbiory.php",         wrapper=zbiory, menubar=Create.html.standard.menubar()), "zbiory"))
