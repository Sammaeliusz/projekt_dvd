<html>
<head>
<link rel="stylesheet" href="{{url_for('static', filename='style.css')}}">
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
    </style>
<script>
    function Zmiana() {
        location.href = './zmiana'
    }
    function zal(){
    let x =document.cookie;
    if (x.includes("zal=yes;"))
        alert("Masz zaległe filmy!");}
</script>

</head>
<body>

{{menubar}}

<div class="powitanie">
        <h1>Cześć, {{user[1]}}! Dobrze cię znów widzieć :)</h1>
        </div>

        <!-- Informacje o użytkowniku -->
        <div class="informacje">
            <table>
                <tr>
                    <td>Nazwa użytkownika: </td>
                    <td>{{user[1]}}</td>
                </tr>
                <tr>
                    <td>Adres e-mail: </td>
                    <td>{{user[2]}}</td>
                </tr>
            </table>
            <button class="gotowe" onclick="Zmiana()">Zmień dane</button>
            <form action="" method="post">
            <button class="gotowe" type="submit" name="logout" value="Wyloguj">Wyloguj</button>
            </form>
        </div>
        <div class="DVD">
        <h2>Wypożyczone Pozycje</h2>
        <table>
            <tr>
                <th>Nazwa</th>
                <th>Okres wypożyczenia</th>
                <th>Czy Film jest zaległy?</th>
            </tr>
            {{swyp}}
        </table>
        </div>
        <div class="DVD">
        <h2>Pozycje wypożyczone w przeszłości</h2>
        <table>
            <tr>
                <th>Nazwa</th>
                <th>Okres wypożyczenia</th>
            </tr>
            {{swypp}}
        </table>
        </div>
        <script>zal();</script>
</body>