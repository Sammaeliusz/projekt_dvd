from flask import Flask
from modules import *
from flask import request
from flask import session
from flask import abort, redirect, url_for
from datetime import date
from datetime import timedelta
app = Flask(__name__)
app.secret_key = b'dgf;hpo4[]t,drgtp[e45.g'
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['id'] = request.form['id']
        return redirect(url_for('panel'))
    return '''
        <form method="post">
            <p><input type=text name=id></p>
            <p><input type=submit value=Login></p>
        </form>
    '''
@app.route('/konto', methods=['GET', 'POST'])
def panel():
    if 'id' in session:
        id = session["id"]
        user = user_finder(conn, id)
        session['user'] = f"{user[1]}|{user[2]}|{user[3]}"
        wyp = wyp_filmy(conn, id)
        swyp = ""
        swypp = ""
        film = []
        dzisiaj = date.today()
        for i in wyp:
            film = film_finder(conn, i[0])
            if i[3] == None and i[2] != None :
                okres = str(i[1].day)+"."+str(i[1].month)+"."+str(i[1].year)+"-"+str(i[2].day)+"."+str(i[2].month)+"."+str(i[2].year)
                if i[2]-dzisiaj < timedelta(0):
                    czy_zalegly = "tak"
                else:
                    czy_zalegly = "nie"
                swyp += f'''
                <tr>
                    <td>{film[1]}</td>
                    <td>{okres}</td>
                    <td>{czy_zalegly}</td>
                </tr>'''
            elif(i[3]!= None):
                okres = str(i[1].day)+"."+str(i[1].month)+"."+str(i[1].year)+"-"+str(i[3].day)+"."+str(i[3].month)+"."+str(i[3].year)
                swypp += f'''
                <tr>
                    <td>{film[1]}</td>
                    <td>{okres}</td>
                </tr>'''
        if request.method == 'POST':
            if (request.form['logout']=="Wyloguj"):
                session.pop('id', None)
                return redirect(url_for('index'))
        return f'''    
        <div class="powitanie">
        <h1>Cze????, {user[1]}! Dobrze ci?? zn??w widzie?? :)</h1>
        </div>

        <!-- Informacje o u??ytkowniku -->
        <div class="informacje">
            <table>
                <tr>
                    <td>Nazwa u??ytkownika: </td>
                    <td>{user[1]}</td>
                </tr>
                <tr>
                    <td>Adres e-mail: </td>
                    <td>{user[2]}</td>
                </tr>
            </table>
            <button onclick="Zmiana()">Zmie?? dane</button>
        </div>
        <div class="DVD">
        <h2>Wypo??yczone Pozycje</h2>
        <table>
            <tr>
                <th>Nazwa</th>
                <th>Okres wypo??yczenia</th>
                <th>Czy Film jest zaleg??y?</th>
            </tr>
            '''+swyp+'''
        </table>
        </div>
        <div class="DVD">
        <h2>Pozycje Wypo??yczone W Przesz??o??ci</h2>
        <table>
            <tr>
                <th>Nazwa</th>
                <th>Okres wypo??yczenia</th>
            </tr>
            '''+swypp+'''
        </table>
        </div>
        <form action="" method="post">
        <input type="submit" name="logout" value="Wyloguj">
        </form>
        <script>
        function Zmiana() {
            location.href = './zmiana'
        }
        </script>
        '''
    return "Co?? nie dzia??a"
@app.route('/zmiana', methods=['GET', 'POST'])
def zmiana():
    if 'user' in session:
        user = session['user']
        id = session['id']
        u = user.split("|")
    if request.method == 'POST':
        if request.form['nazwa']!="":
            u[0]=request.form['nazwa']
        if request.form['mail']!="":
            u[1]=request.form['mail']
        if request.form['passwd']!="":
            u[2]=request.form['passwd']
        user_change_data(conn, id, u)
        return redirect(url_for('panel'))
    return '''<form action="" method="post">
        <table>
            <tr>
                <td>Nazwa: </td>
                <td>E-Mail: </td>
                <td>Has??o:</td>
            </tr>
            <tr>
                <td>Nowa nazwa: <input type="text" name="nazwa" id=""></td>
                <td>Nowy Email: <input type="email" name="mail" id=""></td>
                <td>Nawe has??o: <input type="password" name="passwd" id=""></td>
            </tr>
        </table>
        <input type="submit" value="Zmie??">
    </form>'''
