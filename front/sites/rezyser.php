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

    .searchbar .search {
        display: inline-block;
        border: 0px solid grey;
        padding: 0px;
        transition: all 0.15s ease;
    }
    .searchbar input[type=text] {
        font-size: 14px;
        border: 1px solid #888;
        border-radius: 5px;
        padding: 10px;
        width: 15em;
	    margin: 10px 2px 0 0;
    }

    /* ##### Buttons ##### */
    .btn-group .button {
        background-color: #FFF;
        color: #888;
        padding: 10px;
        text-align: center;
        display: inline-block;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s ease;
        border: 1px solid #888;
        border-radius: 5px;
        margin: 10px 2px;
    }
    .btn-group {
        display: inline-block;
    }
    .btn-group .button:hover {
        background-color: #888;
        color: white;
    }
    .btn-group .button:active, .btn-group .button:focus {
        background-color: #888;
        color: white;
    }

    .container {
        margin: 5px;
        float: left;
        outline: 15px;

    }

    .container img {
        width: 225px;
        height: 300px;
        float: center;
    }

    /* ##### Filter ##### */
    .filterDiv {
        display: none;
    }
    .show {
        display: flex;
    }
    .container-btn {
        margin: 0 0 20px 25px;
        display: flex;
        flex-wrap: wrap;
    }
    .vl {
        border-left: 1px solid lightgrey;
        height: 30px;
        margin: auto 20px;
    }
    </style>
</head>
<body>
    <!-- MENU -->
    {{menubar}}


    <div class="container-btn">
        <div class="searchbar">
            <div class="search">
                <input type="text" id="searchinput" onkeyup="searchFunction()"  placeholder="Search">
            </div>
        </div>
        <div class="vl"></div>
        <div class="buttons">
            <div class="btn-group">
                <button class="button active" onclick="filterSelection('Wszystko')"> Wszystko</button>
                <button class="button" onclick="filterSelection('PReed')"> Peyton Reed</button>
                <button class="button" onclick="filterSelection('JWhedon')"> Joss Whedon</button>
                <button class="button" onclick="filterSelection('Russos')"> Anthony i Joe Russo</button>
                <button class="button" onclick="filterSelection('RCoogler')"> Ryan Coogler</button>
                <button class="button" onclick="filterSelection('JJohnston')"> Joe Johnston</button>
                <button class="button" onclick="filterSelection('BodenFleck')"> Anna Boden and Ryan Fleck</button>
                <button class="button" onclick="filterSelection('SDerrickson')"> Scott Derrickson</button>
                <button class="button" onclick="filterSelection('JWright')"> Jason Wright</button>
                <button class="button" onclick="filterSelection('JGunn')"> James Gunn</button>
                <button class="button" onclick="filterSelection('DWnendt')"> David Wnendt</button>
                <button class="button" onclick="filterSelection('JFavreau')"> Jon Favreau</button>
                <button class="button" onclick="filterSelection('SBlack')"> Shane Black</button>
                <button class="button" onclick="filterSelection('DSandberg')"> David Sandberg</button>
                <button class="button" onclick="filterSelection('HDewin')"> Howie Dewin</button>
                <button class="button" onclick="filterSelection('KAdamik')"> Kasia Adamik</button>
                <button class="button" onclick="filterSelection('JWatts')"> Jon Watts</button>
                <button class="button" onclick="filterSelection('LLeterrier')"> Louis Leterrier</button>
                <button class="button" onclick="filterSelection('KBranagh')"> Kenneth Branaghr</button>
                <button class="button" onclick="filterSelection('ATaylor')"> Alan Taylor</button>
                <button class="button" onclick="filterSelection('TWaititi')"> Taika Waititi</button>
                <button class="button" onclick="filterSelection('BSteere')"> Brendan Steere</button>
                <button class="button" onclick="filterSelection('QDupieux')"> Quentin Dupieux</button>

            </div>
        </div>
    </div>
	

    <!-- Filmy -->
    <div id="filmy">
        <div class="container filterDiv PReed">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Ant-Man.png"></button></a>
                <p>Ant-Man</p>
            </div>
        </div>
	
        <div class="container filterDiv PReed">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Ant-Man-i-Osa.jpg"></button></a>
                <p>Ant-Man i Osa</p>
            </div>
        </div>
    
        <div class="container filterDiv JWhedon">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Avengers.png"></button></a>
                <p>Avengers</p>
            </div>
        </div>

        <div class="container filterDiv JWhedon">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Avengers-Czas-Ultrona.png"></button></a>
                <p>Avengers: Czas Ultrona</p>
            </div>
        </div>

        <div class="container filterDiv Russos">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Avengers-Koniec-Gry.png"></button></a>
                <p>Avengers: Koniec Gry</p>
            </div>
        </div>

        <div class="container filterDiv Russos">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Avengers-Wojna-Nieskonczonosci.png"></button></a>
                <p>Avengers: Wojna Nieskończoności</p>
            </div>
        </div>

        <div class="container filterDiv RCoogler">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Czarna-Pantera.png"></button></a>
                <p>Czarna Pantera</p>
            </div>
        </div>

        <div class="container filterDiv SDerrickson">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Doktor-Strange.png"></button></a>
                <p>Doktor Strange</p>
            </div>
        </div>

        <div class="container filterDiv JWright">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Finding-Jesus.jpg"></button></a>
                <p>Finding Jesus</p>
            </div>
        </div>

        <div class="container filterDiv JWright">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Finding-Jesus-2.jpg"></button></a>
                <p>Finding Jesus 2</p>
            </div>
        </div>

        <div class="container filterDiv JFavreau">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Iron-Man.jpg"></button></a>
                <p>Iron Man</p>
            </div>
        </div>

        <div class="container filterDiv JFavreau">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Iron-Man-2.jpg"></button></a>
                <p>Iron Man 2</p>
            </div>
        </div>

        <div class="container filterDiv SBlack">
        <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Iron-Man-3.png"></button></a>
                <p>Iron Man 3</p>
            </div>
        </div>

        <div class="container filterDiv JJohnston">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Kapitan-Ameryka-Pierwsze-Starcie.png"></button></a>
                <p>Kapitan Ameryka: Pierwsze Starcie</p>
            </div>
        </div>

        <div class="container filterDiv Russos">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Kapitan-Ameryka-Wojna-Bohaterow.png"></button></a>
                <p>Kapitan Ameryka: Wojna Bohaterów</p>
            </div>
        </div>

        <div class="container filterDiv Russos">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Kapitan-Ameryka-Zimowy-Zolnierz.png"></button></a>
                <p>Kapitan Ameryka: Zimowy Żołnierz</p>
            </div>
        </div>
    
        <div class="container filterDiv BodenFleck">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Kapitan-Marvel.png"></button></a>
                <p>Kapitan Marvel</p>
            </div>
        </div>

        <div class="container filterDiv DSandberg">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Kung-Fury.jpg"></button></a>
                <p>Kung Fury</p>
            </div>
        </div>

        <div class="container filterDiv HDewin">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Llamagedon.jpg"></button></a>
                <p>Llamageddon</p>
            </div>
        </div>

        <div class="container filterDiv DWnendt">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Look-Whos-Back.jpg"></button></a>
                <p>Look Who's Back</p>
            </div>
        </div>

        <div class="container filterDiv KAdamik">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Serce-gor.jpg"></button></a>
                <p>Serce Gór</p>
            </div>
        </div>

        <div class="container filterDiv JWatts">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Spider-Man-Daleko-od-domu.png"></button></a>
                <p>Spider-Man: Daleko od domu</p>
            </div>
        </div>

        <div class="container filterDiv JWatts">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Spider-Man-Homecoming.png"></button></a>
                <p>Spider-Man: Homecoming</p>
            </div>
        </div>

        <div class="container filterDiv JGunn">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Straznicy-Galaktyki.png"></button></a>
                <p>Strażnicy Galaktyki</p>
            </div>
        </div>

        <div class="container filterDiv JGunn">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Straznicy-Galaktyki-2.png"></button></a>
                <p>Strażnicy Galaktyki 2</p>
            </div>
        </div>

        <div class="container filterDiv LLeterrier">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/The-Incredible-Hulk.jpeg"></button></a>
                <p>The Incredible Hulk</p>
            </div>
        </div>

        <div class="container filterDiv KBranagh">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Thor.png"></button></a>
                <p>Thor</p>
            </div>
        </div>

        <div class="container filterDiv ATaylor">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Thor-Mroczny-swiat.png"></button></a>
                <p>Thor: Mroczny świat</p>
            </div>
        </div>

        <div class="container filterDiv TWaititi">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Thor-Ragnarok.png"></button></a>
                <p>Thor: Ragnarok</p>
            </div>
        </div>

        <div class="container filterDiv BSteere">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Velocipastor.jpg"></button></a>
                <p>Velocipasotr</p>
            </div>
        </div>

        <div class="container filterDiv QDupieux">
            <div class="content">
                <a href="film.php" target="_blank"><button><img src="Filmy/Zabojcza-opona.jpg"></button></a>
                <p>Zabójcza Opona</p>
            </div>
        </div>
    </div>
    
</body>
</html>
<script>
    filterSelection("Wszystko")

function filterSelection(c) {
    var x, i;
    x = document.getElementsByClassName("filterDiv");
    if (c == "Wszystko") c = "";
    // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
    for (i = 0; i < x.length; i++) {
        w3RemoveClass(x[i], "show");
        if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
    }
}

// Show filtered elements
function w3AddClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        if (arr1.indexOf(arr2[i]) == -1) {
            element.className += " " + arr2[i];
        }
    }
}

// Hide elements that are not selected
function w3RemoveClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
        while (arr1.indexOf(arr2[i]) > -1) {
            arr1.splice(arr1.indexOf(arr2[i]), 1);
        }
    }
    element.className = arr1.join(" ");
}



// get search bar element
const searchInput = document.getElementById("searchinput");

// store name elements in array-like object
const namesFromDOM = document.getElementsByClassName("content");

// listen for user events
searchInput.addEventListener("keyup", (event) => {
    const { value } = event.target;
    
    // get user search input converted to lowercase
    const searchQuery = value.toLowerCase();
    
    for (const nameElement of namesFromDOM) {
        // store name text and convert to lowercase
        let name = nameElement.textContent.toLowerCase();
        
        // compare current name to search input
        if (name.includes(searchQuery)) {
            // found name matching search, display it
            nameElement.style.display = "block";
        } else {
            // no match, don't display name
            nameElement.style.display = "none";
        }
    }
});

</script>