<html>
<head>
<style>
    html {
        background-color: #fff5e3;
    }
    .tab {
        background-color: #7b1212;
        overflow: hidden;
    }

    .tab button {
        background-color: inherit;
        color: #fff5e3;
        float: right;
        border: none;
        outline: none;
        cursor: pointer;
        font-size: 15;
        padding: 20px 20px;
        transition: 0.3s;
    }
    .tab button:hover {
        background-color: #fff5e3;
        color: #7b1212;
    }

    .tab button.active {
        background-color: #ccc;
        color: black;
    }

    .tabcontent {
        background-color: white;
        text-align: justify;
        display: none;
        padding: 70px 70px 70px 70px;
        border: 1px solid #ccc;
        border-top: none;
        font-size: 30px;
    }
    </style>
</head>
<body>
    <div class="tab">
        <button onmouseover="user_icon.png" onclick="openfile(konto.php)"> <img src="user_icon_hover.png" width="17.5" length="17.5"></button>
        <button class="tablinks" onclick="openfile(konto)">FAQ</button>
        <button class="tablinks" onclick="">Kontakt</button>
        <button class="tablinks" onclick="">Zbiory</button>
        <button class="tablinks" onclick="">Strona Główna</button>
    </div>




    <script>
        function openfile(file) { window.location = "file:///C:/xampp/htdocs/projekt/" + file; }
    </script>    
</body>
</html>