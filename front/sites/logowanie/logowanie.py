import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    kwg = Struct(kwg)
    #kwg = Struct(kwg)
    if (mail:=bottle.request.forms.get('mail', None)) and (password:=bottle.request.forms.get('password', None)):
        if (id_user:=sql.login_user(mail, password)) >= 0:
            bottle.response.set_cookie('id', str(id_user))
            bottle.response.set_cookie("user_auth", "placeholder")
            return redirect('/panel')
        else:
            return function(error=id_user, data=kwg.data)
    else:
        return function(data=kwg.data)
