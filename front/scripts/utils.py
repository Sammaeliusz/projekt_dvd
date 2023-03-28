import bottle
from sys import path as system_path

from io import BytesIO
from datetime import date, timedelta
from codebase.sqlConn import SQL
from codebase.uses import Struct

def redirect(location:str) -> bottle.Response:
    try:
        return bottle.redirect(location)
    except bottle.HTTPResponse as res:
        return res

def environhack():
    body = "amogus"
    bottle.request.environ['CONTENT_LENGTH'] = str(len(bottle.tob(body)))
    bottle.request.environ['wsgi.input'] = BytesIO()
    bottle.request.environ['wsgi.input'].write(bottle.tob(body))
    bottle.request.environ['wsgi.input'].seek(0)
