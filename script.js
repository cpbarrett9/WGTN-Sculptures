
// Declaring element variables:
var web_panel;
var leaflet_controls;
var attribution_panel;
var navigation;
var open_eye_svg;
var closed_eye_svg;
var hide_menu_alert;

var fullscreen_button; // <- Fullscreen button + boolean
var isFullscreenActive = false;

// onClick function for menu toggle button:
window.onload = function() {

    // Get elements we want from their id:
    let menu_toggle =       document.getElementById("menu-toggle");
    web_panel =             document.getElementById("web-panel");
    leaflet_controls =      document.getElementsByClassName("leaflet-control-container")[0];
    attribution_panel =     document.getElementById("attribution");
    navigation =            document.getElementById("navigation");
    open_eye_svg =          document.getElementById("open-eye-svg");
    closed_eye_svg =        document.getElementById("closed-eye-svg");
    hide_menu_alert =       document.getElementById("hide-menu-alert");

    // Display closed eye svg initially:
    open_eye_svg.style.visibility = "hidden";
    closed_eye_svg.style.visibility = "visible";
    hide_menu_alert.style.visibility = "hidden";

    // Add event listener to menu toggle button:
    menu_toggle.addEventListener("click", function() {

            // Hide menu:
            if (isMenuToggled) {
                console.log("Menu disabled");
                hideMenu();
            }
            // Show menu:
            else {
                console.log("Menu enabled");
                showMenu()
            }

        }
    );

    // Adding event listener to full screen button:
    let fullscreen_button = document.getElementById("full-screen-button");
    fullscreen_button.addEventListener("click", function(){
        if (isFullscreenActive) {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {  // iOS Safari
                document.webkitExitFullscreen();
            } else if (document.mozCancelFullScreen) {   // Firefox
                document.mozCancelFullScreen();
            } else if (document.msExitFullscreen) {      // IE/Edge
                document.msExitFullscreen();
            }
            isFullscreenActive = false;
        } else {
            // enter fullscreen with vendor prefixes
            const elem = document.documentElement;
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) {   // iOS Safari, Chrome
                elem.webkitRequestFullscreen();
            } else if (elem.mozRequestFullScreen) {      // Firefox
                elem.mozRequestFullScreen();
            } else if (elem.msRequestFullscreen) {       // IE/Edge
                elem.msRequestFullscreen();
            }
            isFullscreenActive = true;
        }
    })

    // Run on load:
    detectMobile(mq);
}

// isMenuToggled(): Tracks if the menu is currently visible
let isMenuToggled = true;

// toggleMenuBoolean(): Call to switch status of the isMenuToggled boolean
function toggleMenuBoolean() {
    if (isMenuToggled) {
        /* When switching to hidden menu: */
        isMenuToggled = false;
        open_eye_svg.style.visibility = "visible"; // <- Switch which eye svg is visible
        closed_eye_svg.style.visibility = "hidden";
    }
    else {
        /* When switching to visible menu: */
        isMenuToggled = true;
        open_eye_svg.style.visibility = "hidden";
        closed_eye_svg.style.visibility = "visible";
    }
        
}

// hideMenu(): Set menu elements to hidden:
function hideMenu() {
    toggleMenuBoolean();
    leaflet_controls.style.visibility = "hidden";
    attribution_panel.style.visibility = "hidden";
    navigation.style.visibility = "hidden";
    web_panel.style.visibility = "hidden";
}

// showMenu(): Set menu elements to visible:
function showMenu() {
    toggleMenuBoolean();
    // If the show menu alert was activated, turn it off:
    if (hide_menu_alert.style.visibility == "visible") {
        hide_menu_alert.style.visibility = "hidden";
    }
    leaflet_controls.style.visibility = "visible";
    attribution_panel.style.visibility = "visible";
    navigation.style.visibility = "visible";
    web_panel.style.visibility = "visible";
}

// <-  Triggering hide menu by default on mobile devices: -->

// Hide menu if the screen is small:
function detectMobile(e) {
    if (e.matches) {
        // Alert shows next to menu toggle on mobile to draw attention to it (invisible by default on mobile)
        hide_menu_alert.style.visibility = "visible";
        hideMenu();
    }
}

// MediaQueryList:
const mq = window.matchMedia('(max-width: 575px)');