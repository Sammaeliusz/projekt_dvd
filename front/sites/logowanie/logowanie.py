import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    
    kwg = Struct(kwg)
    
    if (mail:=bottle.request.forms.get('mail', None)) and (password:=bottle.request.forms.get('password', None)):
        question = sql.user_login(mail, password)
        
        if not question.isError():
            print(question.getList())
            bottle.response.set_cookie('id', str(question.getId()))
            bottle.response.set_cookie("auth", "logging")
            return redirect('/panel')
        
        return function(error=question.getMessage(), data=kwg.data)
    
    return function(data=kwg.data)
