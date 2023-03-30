import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    kwg = Struct(kwg)
    if (user:=bottle.request.get_cookie("user")) and not bottle.request.method == 'POST':
        return function()
    else:
        user = user.split("|")
        to_pass = [x if x != None else user[n] for n, x in enumerate([bottle.request.forms.get('name', None),bottle.request.forms.get('mail', None),bottle.request.forms.get('password', None)])]
        question = sql.userdata_change(bottle.request.get_cookie("id"), *to_pass)
        if question.isInfo():
            return function(error=question.getError(), data=kwg.data)
        else:
            return redirect('/panel')
    
