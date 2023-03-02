<html>
<head>
<link rel="stylesheet" href="{{url_for('static', filename='style.css')}}">
<script>
    function goToURL(adres) {
        window.open(adres);
    }
</script>
</head>
<body>
    <!-- MENU -->
    {{menubar}}
    
    <!-- Intro -->
    <div class="intro_2">
        <h1 class="h1_3">Logowanie</h1>
    </div>

    <!-- Logowanie -->
    <div class="logowanie">
        <form action='logowanie' target='_self' method='post'>
            <div class="okno">
                <label class="etykieta">Email:</label>
                <input name="mail" type="text" autofocus required>
            </div>
            
            <div class="okno">
                <label class="etykieta">Hasło:</label>
                <input id="pass" name="password" type="password" required>
                <a class="reset" href="reset.php">Zapomniałem hasła...</a>
            </div>
            <button class="gotowe" type='submit'>Zaloguj</button>
        </form>
		{% if error is defined %}
			<p class="p_1" style="color:red">Błąd podczas logowania: Error {{error}}</p>
		{% endif %}
        <p class="p_1">Nie masz jeszcze konta? <a class="rejestracja" href="rejestracja">Zarejestruj się!</a></p>
    </div>    


</body>
</html>