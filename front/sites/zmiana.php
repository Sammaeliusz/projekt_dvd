<html>
<head>
<link rel="stylesheet" href="{{url_for('static', filename='style.css')}}">
<script>
    function goToURL(adres) {
        window.open(adres);
    }
    function back(){
        location.href = './panel';
    }
</script>
</head>
<body>
    <!-- MENU -->
    {{menubar}}
    
    <!-- Intro -->
    <div class="intro">
        <h1 class="h1_1">Zmiana danych użytkownika</h1>
    </div>

    <!-- Logowanie -->
    <div class="logowanie">
        <form action='zmiana' target='_self' method='post'>
            <div class="okno">
                <label class="etykieta">Nazwa użytkownika:</label>
                <input name="name" type="text" autofocus>
            </div>
			
			<div class="okno">
                <label class="etykieta">E-mail:</label>
                <input name="mail" type="email">
            </div>
            
            <div class="okno">
                <label class="etykieta">Hasło:</label>
                <input id="pass" name="passwd" type="password">
            </div>
            <button class="gotowe" type='submit' onclick="back()">Zmień</button>
        </form>
		{% if error is defined %}
			<p class="p_1" style="color:red">Błąd podczas zmiany danych: Error {{error}}</p>
		{% endif %}
    </div>    


</body>
</html>