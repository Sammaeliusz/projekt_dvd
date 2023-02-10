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

    .newest_home {
	padding: 10px;
	display: grid;
    grid-template-columns: repeat(5, 300px);
	grid-template-rows: 300px;
	grid-column-gap: 1rem;
	grid-row-gap: 1rem;
	overflow-x: scroll;
    overflow-y: hidden;
	height: 300px;
    float: center;
	scroll-snap-type: both mandatory;
	scroll-padding: 1rem;
    color: #442AAD;
    }

    .newest_home::-webkit-scrollbar {
    display: none;
    }

    .active {
	    scroll-snap-type: unset;
    }

    .newest_home button {
        height: 275px;
	    scroll-snap-align: center;
	    display: inline-block;
	    border-radius: 25px;
	    font-size: 0;
    }

    .popular_home {
        color: #442AAD;
    	padding: 10px;
	    display: grid;
        grid-template-columns: repeat(5, 300px);
	    grid-template-rows: 300px;
	    grid-column-gap: 1rem;
    	grid-row-gap: 1rem;
	    overflow-x: scroll;
        overflow-y: hidden;
	    height: 300px;
        float: center;
	    scroll-snap-type: both mandatory;
	    scroll-padding: 1rem;
    }

    .active {
	    scroll-snap-type: unset;
    }

    .popular_home::-webkit-scrollbar {
    display: none;
    }

    .popular_home button {
        height: inherit;
	    scroll-snap-align: center;
	    display: inline-block;
	    border-radius: 25px;
	    font-size: 0;
    }

    h1 {
        font-size: 40;
        font-family: "Roboto";
        color: #442AAD;
    }

    .intro {
        padding: 50px;
        text-align: center;
        font-size: 25;
        font-family: "Roboto";
        color: #442AAD;
    }
    

    h2 {
        font-family: "Roboto";
        color: #442AAD;
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

    <!-- Intro -->
    <div class="intro">
        <h1>Najlepsza platforma do wypożyczania DVD na świecie!</h1>
        <a>Nieograniczona oferta filmów, seriali, programów i nie tylko. Oglądaj wszędzie. Pobierz ulubione tytuły i oglądaj offline. Zapisz ulubione tytuły, aby zawsze mieć coś do obejrzenia.</a>
    </div>

    <!-- Najnowsze płyty -->
    <h2>Sprawdź nasze najnowsze pozycje!</h2>
    <div class="newest_home">
        <button onclick=""></button>
        <button onclick=""></button>
        <button onclick=""></button>
        <button onclick=""></button>
        <button onclick=""></button>
    </div>

    <!-- Najpopularniejsze płyty -->
    <h2>Chcesz wiedzieć co najczęściej wybierali inni? Oto nasze najpopularniejsze filmy:</h2>
    <div class="popular_home">
        <button onclick=""></button>
        <button onclick=""></button>
        <button onclick=""></button>
        <button onclick=""></button>
        <button onclick=""></button>
    </div>

 
</body>
</html>