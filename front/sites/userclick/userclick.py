import sys
from os import getcwd
sys.path.append('../front/scripts')
from utils import *

def wrapper(function:callable, sql:SQL, **kwg) -> callable:

    if bottle.request.get_cookie('zal'):
        return redirect('/panel')
    return redirect('/logowanie')
