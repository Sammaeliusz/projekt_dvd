import flask
from abc import ABC, abstractmethod
from modules import *
from datetime import date, timedelta
from random import choice
from string import ascii_letters
from os import getcwd
from sitescripts import index, panel, zmiana, userclick, login, register

class App(flask.Flask):
    route_list = []
    def addroute(self, route:callable):
        self.route_list.append(route)
    def setSecret(self, secret_key):
        self.secret_key = secret_key

class Create(ABC):
    class flask(ABC):
        @abstractmethod
        def route(app:flask.Flask, route:str, base_function:callable, route_id:str, methods=['GET','POST'], *args, **kwargs) -> callable:
            @app.route(route, methods=methods, endpoint=route_id)
            def f(*args, **kwargs):
                return base_function(*args, **kwargs)
            return f
        
        @abstractmethod
        def dynamicRoute(app:flask.Flask, route:str, base_function:callable,route_id:str, methods=['GET','POST'], *args, **kwargs) -> callable:
            @app.route(route, methods=methods, endpoint=route_id)
            def f(*args, **kwargs):
                return base_function(*args, **kwargs)
            return f
    class function(ABC):
        @abstractmethod
        def withTemplate(template:str, **kwargs) -> callable:
            return lambda **kwg : flask.make_response(flask.stream_template(template, **{**kwargs, **kwg}))

        @abstractmethod
        def withFunction(function:callable) -> callable:
            return lambda : flask.make_response(function())

    @abstractmethod
    def Wrapper(wrapper:callable, function:callable) -> callable:
        return lambda : wrapper(function)

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
                with open(getcwd()+"/../front/standard/menubar.txt", 'rb') as f:
                    return f.read().decode("utf-8")

app = App(__name__, template_folder='/projekt/front/templates/', static_folder='/projekt/front/data/')
app.setSecret(b'dgf;hpo4[]t,drgtp[e45.g')

#''.join(choice(ascii_letters) for i in range(32))
app.addroute(Create.flask.route(app, '/',               Create.Wrapper(index,    Create.function.withTemplate("index.php",          menubar=Create.html.standard.menubar())), "index"))
app.addroute(Create.flask.route(app, '/panel',          Create.Wrapper(panel,    Create.function.withTemplate("panel.php",          menubar=Create.html.standard.menubar())), 'panel'))
app.addroute(Create.flask.route(app, '/userclick',      Create.function.withFunction(userclick), 'userclick'))
app.addroute(Create.flask.route(app, '/logowanie',      Create.Wrapper(login,    Create.function.withTemplate("logowanie.php",      menubar=Create.html.standard.menubar())), "login"))
app.addroute(Create.flask.route(app, '/zmiana',         Create.Wrapper(zmiana,   Create.function.withTemplate("zmiana.php",         menubar=Create.html.standard.menubar())), "zmiana"))
app.addroute(Create.flask.route(app, '/rejestracja',    Create.Wrapper(register, Create.function.withTemplate("rejestracja.php",    menubar=Create.html.standard.menubar())), "register"))
