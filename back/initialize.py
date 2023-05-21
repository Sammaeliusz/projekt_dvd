import tomllib
import app
#from sys import setrecursionlimit

from codebase.SQL.connect import SQL
from codebase.Tools.structure import Struct

if __name__=="__main__":
    #setrecursionlimit(2000)
    with open("config.conf", "rb") as f:
        config = tomllib.load(f)
        main = config["main"]
        run = config["run"]
        start = Struct(config["start"])
        sql = Struct(config["sql"])
    
    application = app.Application(sql=SQL(username=sql.username, password=sql.password, hostname=sql.hostname, databaseName=sql.dbName), **main)
    application.runApp(**run, debug=start.debug)
