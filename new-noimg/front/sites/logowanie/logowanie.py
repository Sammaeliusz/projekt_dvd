import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable) -> callable:
    #environhack()
    if (mail:=bottle.request.forms.get('mail', None)) and (password:=bottle.request.forms.get('password', None)):
        if (id_user:=user_login(conn, mail, password)) > 0:
            bottle.response.set_cookie('id', str(id_user))
            bottle.response.set_cookie("user_auth", "placeholder")
            return redirect('/panel')
        else:
            return function(error=id_user)
    else:
        return function()
