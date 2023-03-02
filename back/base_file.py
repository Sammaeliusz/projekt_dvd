import flask
from abc import ABC, abstractmethod
from modules import *
from datetime import date, timedelta
from random import choice
from string import ascii_letters
from os import getcwd
from sitescripts import index, panel, zmiana, userclick, login

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
    class mainFunction(ABC):
        @abstractmethod
        def fromTemplate(template:str, **kwargs) -> callable:
            return lambda **kwg : flask.Response(flask.stream_template(template, **{**kwargs, **kwg}))

        @abstractmethod
        def fromFunction(function:callable) -> callable:
            return lambda : flask.Response(function())

    @abstractmethod
    def addWrapper(wrapper:callable, function:callable) -> callable:
        return lambda : wrapper(function)

    class html(ABC):
        class base(ABC):
            @abstractmethod
            def fromFunctions(head:callable,body:callable) -> str:
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
            def fromText(head:str, body:str) -> str:
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

app = App(__name__, template_folder=getcwd()+'\\front\\sites', static_folder=getcwd()+'\\front\\data')
app.setSecret(b'dgf;hpo4[]t,drgtp[e45.g')
with open(getcwd()+"\\back\\data\\menubar.txt", 'rb') as f:
    menubar = f.read().decode("utf-8")

#''.join(choice(ascii_letters) for i in range(32)
app.addroute(Create.flask.route(app, '/', Create.addWrapper(index, Create.mainFunction.fromTemplate("index.php", menubar=menubar)), "index"))
app.addroute(Create.flask.route(app, '/konto', Create.mainFunction.fromFunction(panel), 'panel'))
app.addroute(Create.flask.route(app, '/userclick', Create.mainFunction.fromFunction(userclick), 'userclick'))
app.addroute(Create.flask.route(app, '/logowanie', Create.addWrapper(login, Create.mainFunction.fromTemplate("logowanie.php", menubar=menubar)), "login"))
app.addroute(Create.flask.route(app, '/zmiana', Create.addWrapper(zmiana, Create.mainFunction.fromTemplate("zmiana.php", menubar=menubar)), "zmiana"))
