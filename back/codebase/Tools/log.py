from ..Tools.structure import Struct
from datetime import datetime as datef
from sys import stdout

stream = stdout.write

class loggingSession:

    def __init__(self, name:str, rank:int, form:str, stream:callable, data:Struct):
        self.name = name
        self.rank = rank
        self.form = form
        self.stream = stream
        self.data = data

    def log(self, data:Struct):
        self.data += data
        self.stream(f"{self.name} >>> {self.rank} >>> {datef.now().strftime('us:%f => %H:%M:%Ss <<< ')}" + self.form.format(**self.data.dict()) + '\n')

def log(name:str, data:str, rank=0):
    stream(f"{name} >>> {rank} >>> {datef.now().strftime('us:%f => %H:%M:%Ss <<< ')}" + data + '\n')
