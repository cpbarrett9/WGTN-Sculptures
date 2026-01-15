
/* 
*   TO DO:
*   - Grab and declare necessary elements (menu items to trigger visibility for)
*   - Set those elements invisible/visible
*   - Make the toggle button look nice
*/

// onClick function for menu toggle button
window.onload = function() {
    let menu_toggle = document.getElementById("menu-toggle");
    menu_toggle.addEventListener("click", function() {
            if (isMenuToggled) {
                console.log("Menu disabled");
                toggleMenu();
            }
            else {
                console.log("Menu enabled");
                toggleMenu();
            }
        }
    );
}

// isMenuToggled(): Tracks if the menu is currently visible
let isMenuToggled = true;

// toggleMenu(): Call to switch status of the isMenuToggled boolean
function toggleMenu() {
    if (isMenuToggled) isMenuToggled = false;
    else isMenuToggled = true;
}