import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable) -> callable:
    if (user:=bottle.request.get_cookie("user")):
        user = user.split("|")
        if bottle.request.method == 'POST':
            if (e:=user_change_data(conn, bottle.request.get_cookie("id"), [x if x != None else user[n] for n, x in enumerate([bottle.request.forms.get('name', None),bottle.request.forms.get('mail', None),bottle.request.forms.get('passwd', None)])])) < 0:
                return function(error=e)
            else:
                return redirect('/panel')
    return function(error=None)
