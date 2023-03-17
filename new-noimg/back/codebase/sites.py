from codebase.uses import Struct as Struc
import bottle as bSites

class Site:

    def __init__(self, config:str, name:str, headers:dict, *args, wrapper=(lambda n: n()),**kwargs):
        with open(f"{config}/data.toml", 'rb') as f:
            import tomllib
            self.__config = Struc(tomllib.load(f))
        self.__kwargs = kwargs
        self.name = self.__config.main.name if hasattr(self.__config.main, 'name') else name
        self.__headers = headers
        self.route = self.__config.main.route
        if hasattr(self.__config, 'script'):
            import importlib.util
            spec = importlib.util.spec_from_file_location(self.__config.script.name, f"{config}{self.__config.script.local}")
            script = importlib.util.module_from_spec(spec)
            from sys import modules as sysmod
            sysmod[self.__config.script.name] = script
            spec.loader.exec_module(script)
            self.__wrapper = script.wrapper
        else:
            self.__wrapper = wrapper

    def Answer(self, statuscode=200) -> callable:
        return lambda : self.__wrapper(lambda **kwg : bSites.Response(body = bSites.template(self.__config.main.local, **(vars(self.__config.data) | self.__kwargs | kwg)), headers = self.__headers, status_code = statuscode))
            
