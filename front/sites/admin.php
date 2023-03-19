<html>
<head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">
<style>
    html {
        background-color: #CABEF8;
        font-family: "Roboto";
    }

    .nav {
        background-color: #442AAD;
        overflow: hidden;
        font-family: "Roboto";
    }

    .nav button {
        background-color: inherit;
        color: #CABEF8;
        float: right;
        border: none;
        outline: none;
        cursor: pointer;
        font-size: 15;
        padding: 17px 17px;
        transition: 0.3s;
    }

    .nav button:hover {
        background-color: #8552F7;
        color: #3600AD;
    }

    h1 {
        text-align: center;
        font-size: 40;
        font-family: "Roboto";
        color: #442AAD;
    }

    .wybor {
        text-align: center;
        font-size: 40;
        font-family: "Roboto";
        color: #442AAD;
    }

    .wybor button {
        font-family: inherit;
        font-size: 20;
        font-weight: bold;
        display: block;
        float: center;
        margin: auto;
        background-color: #442AAD;
        color: #CABEF8;
        padding: 20;
        border-color: #CABEF8;
        border-radius: 25px;
        cursor: pointer;
    }

    a {
        text-decoration: none;
    }
    .container{
        display: flex;
    }
    .btns{
        flex: 1;
    }
</style>
</head>
<body>
    <!-- MENU -->

    {{menubar}}
    <div class="nav">
        <button class="tablinks" onclick="">Nazwa/Logo firmy</button>
        <a href="zbiory.php"><button>Zbiory</button></a>
        <a href="uzytkownicy.php"><button>Użytkownicy</button></a>
    </div>

    <!-- Intro -->
    <div class="intro">
        <h1>Witaj administratorze {{user[1]}}</h1>
    </div>
    <!-- Po kliknięciu w któryś z guzików pojawia się odpowiedni div -->
    <div class="wybor">
        <p>Co chcesz teraz zrobić?</p>
        <div class="container">
            <div class="btns">
                <button>Użytkownicy</button>
            </div>
            <div class="btns">
                <button>Zbiory</button>
            </div>
        </div>
    </div>

    <div class="Users">
        <table>
            <tr>
                <th>Id</th>
                <th>Nazwa</th>
                <th>Czy zaległe?</th>
                <th>Zaległe filmy</th>
                <th>Ban:</th>
            </tr>
            <tr>
                <td>{{Id}}</td>
                <td>{{Nazwa}}</td>
                <td>{{zalagle_bool}}</td>
                <td>{{zalegle_list}}</td>
                <td><button>Banuj</button></td>
            </tr>
        </table>
    </div>
    <div class="Films">
        <table>
            <tr>
                <th>
                    Id
                </th>
                <th>
                    Tytuł
                </th>
                <th>
                    Gatunek
                </th>
                <th>
                    Kategoria Wiekowa
                </th>
                <th>
                    Reżyser
                </th>
                <th>
                    Rok Produkcji
                </th>
                <th>
                    Ilość
                </th>
                <th>Modyfikuj:/Dodaj:</th>
                <th>
                    Usuń:
                </th>
            </tr>
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
        </table>
    </div>
 
</body>
</html>