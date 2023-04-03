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
     ft = """
          <tr>
               <td>{{id}}</td>
               <td><input type="text" name="tytul" id="" value={{tytul}}></td>
               <td><input type="text" name="gatunek" value={{gatunek}}></td>
               <td><input type="text" name="kat_wiek" value={{kat_wiek}}></td>
               <td><input type="text" name="rezyser" value={{rezyser}}></td>
               <td><input type="text" name="rok_prod" value={{rok_prod}}></td>
               <td><input type="text" name="ilosc" value={{ilosc}}></td>
               <td><button>Modyfikuj film</button></td>
               <td><button>Usuń film</button></td>
          </tr>
          """
     ff = """
          <tr>
               <td>{{id}}</td>
               <td><input type="text" name="tytul" id="" value={{tytul}}></td>
               <td><input type="text" name="gatunek" value={{gatunek}}></td>
               <td><input type="text" name="kat_wiek" value={{kat_wiek}}></td>
               <td><input type="text" name="rezyser" value={{rezyser}}></td>
               <td><input type="text" name="rok_prod" value={{rok_prod}}></td>
               <td><input type="text" name="ilosc" value={{ilosc}}></td>
               <td><button>Dodaj film</button></td>
          </tr>
     """
     
     return function()