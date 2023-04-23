import sys
sys.path.append('../front/scripts')
from utils import *
def wrapper(function:callable, sql:SQL, **kwg) -> callable:
    #standard zapisywania kryteriów w ciasteczku: S:nazwisko_rezysera|Y:rok_produkcji|C:category
    crit = bottle.request.get_cookie("critery")
    if crit:
        films = sql.
        tile = f"""
            <div class="container filterDiv \Akcja Sci-Fi\">
                <div class="content">
                    <a href="film" target="_blank"><button><img src="/static/Filmy/\Ant-Man 2015/ANT-MAN_2015.png\"></button></a>
                    <p>Ant-Man</p>
                </div>
            </div>
        """
    else:
