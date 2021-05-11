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
    for (var a = 0; a < strips.length; a++) {
        strips[a].style.backgroundColor = my_color;
    }
}

function to_share(){
    document.getElementsByTagName('svg')[0].remove();
    document.getElementById('container').remove();
    naglowek = document.styleSheets[0].cssRules[1].style;
    naglowek.removeProperty('margin');
    document.styleSheets[0].addRule("#nagłówek", "margin: 2px");
    document.getElementsByTagName("button")[0].remove() ;

    title = document.getElementById("nagłówek");
    dt = document.getElementById("story-title");
    dd = document.getElementById('story-content');

    title.style.fontSize = "50px"
    dd.style.fontSize = "27px"
    dt.style.fontSize = "37px"
}