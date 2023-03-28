import sys
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    #environhack()
    print(bottle.request.body.getvalue().decode('utf-8'))
    if (mail:=bottle.request.forms.get('mail', None)) and (password:=bottle.request.forms.get('password', None)) and (name:=bottle.request.forms.get('name', None)):
        if (id_user:=sql.new_user(name, mail, password)) >= 0:
            bottle.response.set_cookie('id', str(id_user))
            bottle.response.set_cookie("user_auth", "placeholder")
            return redirect('/panel')
        else:
            print(id_user)
            return function(error=id_user)
    else:
        return function(error=None)
