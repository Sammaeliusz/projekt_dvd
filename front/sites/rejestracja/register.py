import sys
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    
    kwg = Struct(kwg)
    
    if (mail:=bottle.request.forms.get('mail', None)) and (password:=bottle.request.forms.get('password', None)) and (name:=bottle.request.forms.get('name', None)):
        question = sql.new_user(name, mail, password)
        if question.isUsefull():
            print(question.getList())
            bottle.response.set_cookie('id', str(question.getId()))
            bottle.response.set_cookie("user_auth", "placeholder")
            return redirect('/panel')
        
        return function(error=question.getMessage(), data=kwg.data)
        
    return function(data=kwg.data)

