<html>
<head>
<link rel="stylesheet" href="{{url_for('static', filename='style.css')}}">
</head>
<body>
    <!-- MENU -->
    {{menubar}}

    <!-- Intro -->
    <div class="intro_1">
        <h1 class="h1_1">Rejestracja</h1>
        <a>W paru prostych krokach zyskaj nielimitowany dostęp do naszych zbiorów. Twój pierwszy wieczór filmowy jest już na wyciągnięcie ręki! Zarejestruj się poniżej, a następnie aktywuj konto poprzez wiadomość wysłaną na Twój adres e-mail.</a>
    </div>

    <!-- Rejestracja -->
    <div class="rejestracja_1">
        <form method="POST" autocomplete="off">
            <div class="okno">
                <label class="etykieta" for="username">Nazwa użytkownika</label>
                <input class="" type="text" name="name" id="username" required />
            </div>
            
            <div class="okno">
                <label class="etykieta" for="email">E-mail</label>
                <input class="" type="email" name="email" id="email" required />
            </div>

            <div class="okno">
                <label class="etykieta" for="password">Hasło</label>
                <input class="" type="password" name="password" id="password" required>
            </div>
            <button class="gotowe" type="submit">ZAREJESTRUJ</button>
        </form>
		{% if error is defined %}
			<p class="p_1" style="color:red">Błąd podczas rejestracji: Error {{error}}</p>
		{% endif %}
        <p class="p_1">Masz już u nas konto? <a class="logowanie_1" href="logowanie">Zaloguj się<a></p>
    </div>

</body>
</html>