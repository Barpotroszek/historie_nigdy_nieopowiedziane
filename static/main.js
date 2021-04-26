function change_menu() {
    console.log("Jest");
    var my_color = "#00d9ff";
    var title = document.getElementById("menu-title")
    var strips = document.getElementsByClassName("menu-button")
    var element = document.getElementById('menu-elements');
    console.log(element);
    var style = getComputedStyle(element)
    console.log(style.color)
    if (style.display == "none") {
        element.style.display = "block";
    }
    else {
        element.style.display = "none";
        my_color = "white";
    }
    
    title.style.color = my_color;
    for (a = 0; a < strips.length; a++) {
        strips[a].style.backgroundColor = my_color;
    }
}