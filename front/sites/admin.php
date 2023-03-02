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

</style>
</head>
<body>
    <!-- MENU -->
    <div class="nav">
        <button class="tablinks" onclick="">Nazwa/Logo firmy</button>
        <a href="zbiory.php"><button>Zbiory</button></a>
        <a href="uzytkownicy.php"><button>Użytkownicy</button></a>
    </div>

    <!-- Intro -->
    <div class="intro">
        <h1>Witaj po stronie administratora!</h1>
    </div>

    <div class="wybor">
        <p>Co chcesz teraz zrobić?</p>
        <a href="uzytkownicy.php"><button>Użytkownicy</button></a>
        <a href="zbiory.php"><button>Zbiory</button></a>
    </div>

 
</body>
</html>