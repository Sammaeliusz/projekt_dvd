import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    kwg = Struct(kwg)
    if (mail:=bottle.request.forms.get('mail', None)) and (password:=bottle.request.forms.get('password', None)):
        question = sql.login_user(mail, password)
        if not question.isInfo():
            bottle.response.set_cookie('id', str(question.getId()))
            bottle.response.set_cookie("user_auth", "placeholder")
            if question.admin():
                return redirect('/admin')
            return redirect('/panel')
        else:
            return function(error=question.getError(), data=kwg.data)
    else:
        return function(data=kwg.data)