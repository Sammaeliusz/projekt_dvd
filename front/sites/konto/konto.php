<html>
<head>
<link rel="stylesheet" href="/static/style.css">
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">

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
</head>
<body>
    <!-- MENU -->
    {{menubar}}

    <div class="powitanie">
        <h1>Cześć, Nazwa! Dobrze cię znów widzieć :)</h1>
    </div>

    <!-- Informacje o użytkowniku -->
    <div class="informacje">
        <table>
            <tr class="tr_1">
                <td class="td_1">Nazwa użytkownika: </td>
                <td class="td_1">Nazwa</td>
            </tr>
            <tr class="tr_1">
                <td class="td_1">Adres e-mail: </td>
                <td class="td_1">adres@email.com</td>
            </tr>
        </table>
        <button onclick="Zmiana()">Zmień dane</button>
    </div>

    <!-- Informacje o wypożyczonych filmach -->
    <div class="DVD">
        <h2 class="h2_1">Wypożyczone Pozycje</h2>
        <table>
            <tr class="tr_1">
                <th class="th_1">Nazwa</th>
                <th class="th_1">Okres wypożyczenia</th>
                <th class="th_1">Zaleganie</th>
            </tr>
            <tr class="tr_1">
                <td class="td_1">Jakiś film</td>
                <td class="td_1">20-30.01.2023</td>
                <td class="td_1">Zalegasz 5 dni - 2137 złotych kary</td>
            </tr>
            <tr class="tr_1">
                <td class="td_1">Jakiś film</td>
                <td class="td_1">20-30.01.2023</td>
                <td class="td_1">Zalegasz 5 dni - 2137 złotych kary</td>
            </tr>
            <tr class="tr_1">
                <td class="td_1">Jakiś film</td>
                <td class="td_1">20-30.01.2023</td>
                <td class="td_1">Zalegasz 5 dni - 2137 złotych kary</td>
            </tr>
        </table>

    </div>
</body>
</html>

