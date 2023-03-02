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
        padding: 20 20 50 20;
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
    .rejestracja {
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

    .logowanie {
        color: #CABEF8;
        font-size: 18;
    }

    .aktywacja {
        text-decoration: none;
    }
    </style>
</head>
<body>
    <!-- MENU -->
    {{menubar}}

    <!-- Intro -->
    <div class="intro">
        <h1>Rejestracja</h1>
        <a>W paru prostych krokach zyskaj nielimitowany dostęp do naszych zbiorów. Twój pierwszy wieczór filmowy jest już na wyciągnięcie ręki! Zarejestruj się poniżej, a następnie aktywuj konto poprzez wiadomość wysłaną na Twój adres e-mail.</a>
    </div>

    <!-- Rejestracja -->
    <div class="rejestracja">
        <form autocomplete="off">
            <div class="okno">
                <label class="etykieta" for="username">Nazwa użytkownika</label>
                <input class="" type="text" name="username" id="username" required />
            </div>
            
            <div class="okno">
                <label class="etykieta" for="email">E-mail</label>
                <input class="" type="email" name="email" id="email" required />
            </div>

            <div class="okno">
                <label class="etykieta" for="password">Hasło</label>
                <input class="" type="password" name="password" id="password" required/>
            </div>
            <button class="gotowe" onclick="open('aktywacja.php')">ZAREJESTRUJ</button>
        </form>
        <p>Masz już u nas konto? <a class="logowanie" href="logowanie.php">Zaloguj się<a></p>
    </div>

</body>
</html>