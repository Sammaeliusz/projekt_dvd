import flask
from abc import ABC, abstractmethod
from modules import *

class App(flask.Flask):
    route_list = []
    def addroute(self, route:callable):
        self.route_list.append(route)

class Create(ABC):
    class flask(ABC):
        @abstractmethod
        def route(app:flask.Flask, route:str, base_function:callable, methods=['GET'], *args, **kwargs) -> callable:
            @app.route(route, methods=methods)
            def f(*args, **kwargs):
                return base_function(*args, **kwargs)
            return f
        
        @abstractmethod
        def dynamicRoute(app:flask.Flask, route:str, base_function:callable, methods=['GET'], *args, **kwargs) -> callable:
            @app.route(route, methods=methods)
            def f(*args, **kwargs):
                return base_function(*args, **kwargs)
            return f
    class mainFunction(ABC):
        @abstractmethod
        def fromTemplate(template:str) -> callable:
            return lambda : flask.Response(flask.stream_template(template))

app = App(__name__, template_folder='./../front', static_folder='./../front')

app.addroute(Create.flask.route(app, '/', Create.mainFunction.fromTemplate("index.html")))