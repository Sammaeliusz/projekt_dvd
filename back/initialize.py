import tomllib
import app
from codebase.sqlConn import SQL, basic
from codebase.uses import Struct

if __name__=="__main__":
    with open("config.conf", "rb") as f:
        config = tomllib.load(f)
        main = config["main"]
        run = config["run"]
        start = Struct(config["start"])
        sql = Struct(config["sql"])

    """match config:
        case {"main": {"secret": str(), "static_folder": str(), "template_folder": str()},
              "run": {"host": str(), "port": int()},
              "start": {"debug":bool()}}:
            main = config["main"]
            run = config["run"]
            start = config["start"]
        case _:
            raise ValueError(f"invalid configuration: {config}")"""
    application = app.Application(sql=SQL(username=sql.username, password=sql.password, hostname=sql.hostname, databaseName=sql.dbName), **main)
    application.runApp(**run, debug=start.debug)
