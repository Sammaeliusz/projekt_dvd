import sys
sys.path.append('../front/scripts')
from utils import *
import requests
def wrapper(function:callable, sql:SQL, **kwg) -> callable:

     user_id = bottle.request.get_cookie("id")
     
     if user_id:
        user_id = int(user_id)

        user = sql.user_finder(user_id)
        
        if user.isUsefull():
          movies = sql.movies_recent(9999)
          users = sql.users_all()

          if movies.isUsefull() and users.isUsefull():
               movies = movies.getList()
               if not isinstance(movies[0], list):
                    movies = [movies]
               
               for y, x in enumerate(movies.copy()):
                    q = sql.movie_tags(movies[y][0])
                    if q.isUsefull():
                         l = []
                         for z in q.getList():
                              l.append(z)
                         movies[y].append(l)
                    else:
                         movies[y].append([])
               users = users.getList()
               if not isinstance(users[0], list):
                    users = [users]
               data=bottle.request.forms.getunicode("data", None)
               if data != None:
                    data = data.split(";")
                    print(data)
                    if len(data)>=8:
                         oper = data.pop()
                    if oper == "add":
                         sql.movie_add(data[1], data[2], data[3], data[4], data[5], data[6], data[7])
                         bottle.response.set_cookie('red', "redi")
                         return redirect('/admin')
               banid=bottle.request.forms.getunicode("banid", None)
               if banid != None:
                    if sql.inactivity_check(banid)!=1:
                         sql.user_unban(banid)
                         bottle.response.set_cookie('red', "redi")
                         return redirect('/admin')
                    else:
                         sql.user_ban(banid)
                         bottle.response.set_cookie('red', "redi")
                         return redirect('/admin')
               user_list = []
               for x in users:
                    q = sql.user_have_return(int(x[0]), today())
                    p_list = []
                    if q.isUsefull():
                         q = q.getList()
                         if not isinstance(q[0], list):
                              q = [q]
                         for y in q:
                              p = sql.movie_finder(int(y[1]))
                              if p.isUsefull():
                                   p_list.append(p.getList()[1])
                    user_list.append([x[0],x[1], p_list, sql.ban_check(int(x[0]))])

               return function(movies = movies, users = user_list, title = kwg['data'].title, user = user.getList()[1])
          return function(movies = [], users = users, title = kwg['data'].title, user = user.getList()[1])
     return redirect('/')

     film_tab = ""
     user_tab = ""
     us_id = bottle.request.get_cookie("id")
     ad = sql.admin(us_id)
     if ad:
          am = sql.all_from_all("movie")
          au = sql.all_from_all("user")
          k = 0
          data=bottle.request.forms.getunicode("data", None)
          if data != None:
               data = data.split(";")
               print(data)
               if len(data)>=8:
                    oper = data.pop()
               if len(data)>=7:
                    img = data.pop()
                    
               file = bottle.request.files.get('obraz')  # Pobierz plik z formularza
               if file:
                    fname, fext = path.splitext(file.filename)
                    if fext != '.png':
                         print('Niepoprawny format pliku.')
                    else:
                         save_path = "../front/data/Filmy"
                         if not path.exists(save_path):
                            makedirs(save_path)
                         file.save(f'{save_path}/{file.filename}')
                         print('Plik {filename} został przesłany i zapisany na serwerze.')
                         
               if oper == "mod":
                    sql.movie_change(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
                    bottle.response.set_cookie('red', "redi")
                    return redirect('/admin')
               elif oper == "add":
                    sql.movie_add(data[1], data[2], data[3], data[4], data[5], data[6], data[7])
                    bottle.response.set_cookie('red', "redi")
                    return redirect('/admin')
               elif oper == "del":
                    sql.movie_delete(data[0])
                    bottle.response.set_cookie('red', "redi")
                    return redirect('/admin')
               print(data)
               print(oper)
          banid=bottle.request.forms.getunicode("banid", None)
          if banid != None:
               if sql.inactivity_check(banid).getList()[0]!=1:
                    sql.user_unban(banid)
                    bottle.response.set_cookie('red', "redi")
                    return redirect('/admin')
               else:
                    sql.user_delete(banid)
                    bottle.response.set_cookie('red', "redi")
                    return redirect('/admin')
          for bm in am.getList():
               fil = f"static/Filmy/{bm[1].replace(' ', '-')}.png"
               if bm == None:
                    break
               film_tab += f"""
                    <tr>
                         <form name="filmy{bm[0]}"  method="post" enctype="multipart/form-data">
                              <td><input type="number" class="film{bm[0]}"name="id" hidden value="{bm[0]}">{bm[0]}</td>
                              <td><input type="text" class="film{bm[0]}" name="tytul" id="" value="{bm[1]}"></td>
                              <td><input type="text" class="film{bm[0]}" name="gatunek" value="{bm[2]}"></td>
                              <td><input type="number" class="film{bm[0]}" name="kat_wiek" value="{bm[3]}"></td>
                              <td><input type="text" class="film{bm[0]}" name="rezyser" value="{bm[4]}"></td>
                              <td><input type="number" class="film{bm[0]}" name="rok_prod" value="{bm[5]}"></td>
                              <td><input type="number" class="film{bm[0]}" name="ilosc" value="{bm[6]}"></td>
                              <td><textarea name="opis" id="" class="film{bm[0]}" cols="50" rows="2">{bm[7]}</textarea></td>
                              <td><img src={fil} width="50" height="75"><input type="file" name="obraz" class="film{bm[0]}" id="" accept=".png"></td>
                              <td><button class="filmmod" id="mod{bm[0]}" type="submit">Modyfikuj film</button></td>
                              <td><button class="filmdel" id="del{bm[0]}">Usuń film</button></td>
                         </form>
                    </tr>
                    """
               k = bm[0]
          nid = k+1
          film_tab += f"""
          <tr>
               <td><input type="number" class="film{nid}"name="id" hidden value="{nid}">{nid}</td>
               <td><input type="text" class="film{nid}"name="tytul" id="" value=></td>
               <td><input type="text" class="film{nid}"name="gatunek" value=></td>
               <td><input type="number" class="film{nid}"name="kat_wiek" value=></td>
               <td><input type="text" class="film{nid}"name="rezyser" value=></td>
               <td><input type="number" class="film{nid}"name="rok_prod" value=></td>
               <td><input type="number" class="film{nid}"name="ilosc" value=></td>
               <td><textarea name="opis" class="film{nid}"id="" cols="50" rows="2"></textarea></td>
               <td><input type="file" class="film{nid} name="obraz" id="" accept=".png"></td>
               <td><button class="filmadd" id="add{nid}" type="submit">Dodaj film</button></td>
          </tr>
          """  
          for bu in au.getList():
               mr = sql.movies_rented(bu[0])
               zf = ""
               if sql.inactivity_check(bu[0]).getList()[0]==1:
                    bou = "B"
               else:
                    bou = "Unb"
               if mr.isUsefull():
                    z = mr.getList()
                    for i in z:
                        f= sql.movie_finder(i[0])
                        if f.isUsefull():
                            zf += f.getList()[1]+", "
               else:
                    z = "brak"
               user_tab += f"""
                    <tr>
                         <td>{bu[0]}</td>
                         <td>{bu[1]}</td>
                         <td>{mr.hasData()}</td>
                         <td>{zf}</td>
                         <td><button class="ban" id="{bu[0]}">{bou}anuj</button></td>
                    </tr>
               """
          return function(user="Admin", movies=film_tab, users=user_tab)
     else:
          return redirect('/panel')
#src="{{'/static/Filmy/'+x[1].replace(' ', '-').replace(':','')+'.png'}}"