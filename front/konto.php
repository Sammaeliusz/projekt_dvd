<html>
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
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

    .powitanie {
        font-family: "Roboto";
        color: #442AAD;
        font-size: 20;
        text-align: center;
        margin: auto;
    }

    .informacje {
        margin-left: 130px;
        position: relative;
        display: block;
        padding: 20;
        float: left;
        background-color: #442AAD;
        width: 500;
        border-width: 50;
        border-color: #CABEF8;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-radius: 20px;
        text-align: center;
    }

    td {
        padding: 10;
        font-family: "Roboto";
        color: #CABEF8;
        text-align: center;
        font-size: 20;
        width: 200;
    }

    th {
        padding: 10;
        font-family: "Roboto", bold;
        color: #CABEF8;
        text-align: center;
        font-size: 20;
        width: 200;
    }

    .informacje button{
        font-family: inherit;
        font-size: 20;
        font-weight: bold;
        display: block;
        float: center;
        background-color: #CABEF8;
        color: #442AAD;
        padding: 20;
        margin: 20;
        border-color: inherit;
        border-radius: 25px;
        cursor: pointer;
    }

    h2 { 
        display: block;
        padding: 10;
        font-family: "Roboto";
        background-color: #CABEF8;
        color: #442AAD;
        font-size: 30;
        text-align: center;
        margin: auto;
        border-color: inherit;
        border-radius: 25px;
    }

    .DVD {
        margin-left: 150px;
        display: block;
        padding: 20;
        float: left;
        background-color: #442AAD;
        width: 500;
        border-width: 50;
        border-color: #CABEF8;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-radius: 20px;
        text-align: center;
    }
    </style>
</head>
<body>
    <!-- MENU -->
    <div class="nav">
        <a href="logowanie.php"><button><img src="proba.png" width="17.7" length="17.7"></button></a>
        <button class="tablinks" onclick="">FAQ</button>
        <button class="tablinks" onclick="">Kontakt</button>
        <a href="zbiory.php"><button>Zbiory</button></a>
        <a href="index.php"><button>Strona Główna</button></a>
    </div>

    <div class="powitanie">
        <h1>Cześć, Nazwa! Dobrze cię znów widzieć :)</h1>
    </div>

    <!-- Informacje o użytkowniku -->
    <div class="informacje">
        <table>
            <tr>
                <td>Nazwa użytkownika: </td>
                <td>Nazwa</td>
            </tr>
            <tr>
                <td>Adres e-mail: </td>
                <td>adres@email.com</td>
            </tr>
        </table>
        <button onclick="Zmiana()">Zmień dane</button>
    </div>

    <!-- Informacje o wypożyczonych filmach -->
    <div class="DVD">
        <h2>Wypożyczone Pozycje</h2>
        <table>
            <tr>
                <th>Nazwa</th>
                <th>Okres wypożyczenia</th>
                <th>Zaleganie</th>
            </tr>
            <tr>
                <td>Jakiś film</td>
                <td>20-30.01.2023</td>
                <td>Zalegasz 5 dni - 2137 złotych kary</td>
            </tr>
            <tr>
                <td>Jakiś film</td>
                <td>20-30.01.2023</td>
                <td>Zalegasz 5 dni - 2137 złotych kary</td>
            </tr>
            <tr>
                <td>Jakiś film</td>
                <td>20-30.01.2023</td>
                <td>Zalegasz 5 dni - 2137 złotych kary</td>
            </tr>
        </table>

    </div>
    <script>
    function Zmiana() {
        var x = document.getElementById("myDIV");
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }
    </script>
</body>
</html>

