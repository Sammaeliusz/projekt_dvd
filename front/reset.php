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

    .informacja {
        font-family: "Roboto";
        color: #442AAD;
        font-size: 30;
        text-align: center;
        margin: auto;
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
        <button class="tablinks" onclick="_top">Strona Główna</button>
    </div>
    <!-- Informacja -->
    <div class="informacja">
        <p>Na twój adres e-mail został wysłany link do zmiany hasła.</p>
        <img src="starting-rocket.png">
        <br>
        <a href="logowanie.php">Powrót do strony logowania</a>
    </div>