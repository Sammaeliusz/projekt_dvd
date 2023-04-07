import sys
sys.path.append('../front/scripts')
from utils import *
def wrapper(function:callable, sql:SQL, **kwg) -> callable:
     ut = """
          <tr>
               <td>{{id}}</td>
               <td>{{nazwa}}</td>
               <td>{{zalagle_bool}}</td>
               <td>{{zalegle_list}}</td>
               <td><button>Banuj</button></td>
          </tr>
          """
     film_tab = ""
     user_tab = ""
     us_id = bottle.request.get_cookie("id")
     ad = sql.admin(us_id)
     print(ad.list())
     if ad:
          am = sql.all_movie()
          k = 0
          for bm in am.list():
               print(film_tab)
               if bm == None:
                    break
               film_tab += f"""
                    <tr>
                         <td>{bm[0]}</td>
                         <td><input type="text" name="tytul" id="" value={bm[1]}></td>
                         <td><input type="text" name="gatunek" value={bm[2]}></td>
                         <td><input type="text" name="kat_wiek" value={bm[3]}></td>
                         <td><input type="text" name="rezyser" value={bm[4]}></td>
                         <td><input type="text" name="rok_prod" value={bm[5]}></td>
                         <td><input type="text" name="ilosc" value={bm[6]}></td>
                         <td><button>Modyfikuj film</button></td>
                         <td><button>Usuń film</button></td>
                    </tr>
                    """
               k+=1
          nid = k
          film_tab += f"""
          <tr>
               <td>{nid}</td>
               <td><input type="text" name="tytul" id="" value=></td>
               <td><input type="text" name="gatunek" value=></td>
               <td><input type="text" name="kat_wiek" value=></td>
               <td><input type="text" name="rezyser" value=></td>
               <td><input type="text" name="rok_prod" value=></td>
               <td><input type="text" name="ilosc" value=></td>
               <td><button>Dodaj film</button></td>
          </tr>
          """  
          return function(user="Admin", film_table=film_tab, user_table=user_tab)
     else:
          return redirect('/panel')
