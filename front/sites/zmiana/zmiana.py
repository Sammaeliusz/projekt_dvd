import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    
    kwg = Struct(kwg)
    user = bottle.request.get_cookie("user")
    
    if user and not bottle.request.method == 'POST':
        return function()
    
    user = user.split("|")
    to_pass = [bottle.request.forms.get('name', None),bottle.request.forms.get('mail', None),bottle.request.forms.get('password', None).replace("\"", "")]
    print(to_pass)
    question = sql.userdata_change(int(bottle.request.get_cookie("id")), *to_pass)
    
    if not question.isUsefull():
        return function(error=question.getMessage(), data=kwg.data)
    
    return redirect('/panel')
    