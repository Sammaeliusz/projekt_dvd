<html>
<head>
	<meta charset="utf-8">
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
    {{!menubar}}

    <div class="wybor">
        <p> W jaki sposób chcesz przeglądać nasze zbiory?</p>
        <a href="kategorie"><button>Kategoria</button></a>
        <a href="rezyser"><button>Reżyser</button></a>
        <a href="rok"><button>Rok produkcji</button></a>
    </div>

</body>
</html>
