<html>
<head>
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

    .intro {
        padding: 20;
        text-align: center;
        font-size: 25;
        font-family: "Roboto";
        color: #442AAD;
    }

    p {
        text-align: center;
        font-size: 18;
        font-family: "Roboto";
        color: #CABEF8;
    }

    .logowanie {
        position: relative;
        display: block;
        padding: 50;
        float: center;
        margin: auto;
        background-color: #442AAD;
        width: 500;
        border-width: 50;
        border-color: #CABEF8;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-radius: 20px;
    }

    .okno {
        background-color: #442AAD;
        display: flex;
        flex-direction: column;
        width: 100%;
        position: relative;
        margin-bottom: 50px;
    }
    
    .okno:before {
        content: "";
        display: inline-block;
        width: 0px;
        height: 2px;
        background-color: #442AAD;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        transition: all 0.4s ease;
    }

    .etykieta {
        background-color: #442AAD;
        color: #CABEF8;
        font-family: "Roboto";
        font-size: 20;
    }

    .gotowe {
        font-family: inherit;
        font-size: 20;
        font-weight: bold;
        display: block;
        float: center;
        margin: auto;
        background-color: #CABEF8;
        color: #442AAD;
        padding: 20;
        border-color: inherit;
        border-radius: 25px;
        cursor: pointer;
    }
    .reset {
        color: #CABEF8;
        font-size: 18;
        text-align: left;
    }

    .rejestracja {
        color: #CABEF8;
        font-size: 18;
    }

    .przycisk{
        text-decoration: none;
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
    
    <!-- Intro -->
    <div class="intro">
        <h1>Logowanie</h1>
    </div>

    <!-- Logowanie -->
    <div class="logowanie">
        <form action='konto.php' target='_self' method='post'>
            <div class="okno">
                <label class="etykieta">E-mail:</label>
                <input name="email" type="email" autofocus>
            </div>
            
            <div class="okno">
                <label class="etykieta">Hasło:</label>
                <input id="pass" name="password" type="password">
                <a class="reset" href="reset.php">Zapomniałem hasła...</a>
            </div>
            <button class="gotowe" type='submit'>Zaloguj</button>
        </form>
        <p>Nie masz jeszcze konta? <a class="rejestracja" href="rejestracja.php">Zarejestruj się!</a></p>
    </div>    


</body>
</html>
<script>
    function goToURL(adres) {
        window.open(adres);
    }
</script>