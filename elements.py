import folium
import pandas as pd
from folium import Element
from folium.plugins import Search, LocateControl
import elements

#
#   'elements': Library of functions that return web elements that may be used by multiple maps (css styling, etc)
#   Cleans up scripts that might otherwise be bogged down by long strings.
#

# Returns CSS that should go to the top of every (or many) map pages.
def global_css():
    return """
    <style>

        .leaflet-control-search {
            z-index: 9999 !important;
        }

        .leaflet-popup-content-wrapper {
            /*z-index: 10000 !important;*/
        }

        /* Optimizing for mobile devices: */
        @media only screen and (max-width: 870px) {

            /* Hide web panel */
            #web-panel {
                display: none;
            }

            /* Resize popups: */
            .leaflet-popup-content {
                width: 330px;
            }
            .leaflet-popup-content iframe {
                width: 330px;
            }

            /* Hide desktop version of the popups */
            .leaflet-popup-content iframe .popup-desktop {
                display: none;
            }
        }

        .eye-svg-toggle {
            position: relative;
            width: 25px;
            height: 25px;
        }

        .eye-svg-toggle svg {
            position: absolute;
            inset: 0;
        }

    </style>
    """
# Removes unwanted underline from SVG links:
def remove_underline():
    return """

            .icon-links a {
            text-decoration: none;
        }

    """
# Returns button to toggle/untoggle on-screen menu options:
def hide_menu_toggle():
    return f"""

    <script src="script.js"></script>
    <div style="
        position: fixed;
        bottom: 12px;
        right: 12px;
        z-index: 9999;
        background-color: white;
        padding: 10px 10px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.3);
        font-family: Arial, sans-serif;
    ">
        <button id="menu-toggle" aria-label="Toggle Menu" style="
            background: none;
            color: inherit;
            border: none;
            padding: 0;
            margin: 0;
            font: inherit;
            cursor: pointer;
            outline: inherit;
            font-size: 9px;
        ">
            <div class="eye-svg-toggle">
                <svg xmlns="http://www.w3.org/2000/svg" id="open-eye-svg" 
                    width="28" 
                    height="28" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="2" 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    class="lucide lucide-eye-icon lucide-eye">
                    <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/>
                    <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg xmlns="http://www.w3.org/2000/svg" id="closed-eye-svg" 
                    width="28" 
                    height="28" 
                    viewBox="0 0 24 24"
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="2" 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    class="lucide lucide-eye-off-icon 
                    lucide-eye-off">
                    <path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/>
                    <path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/>
                    <path d="m2 2 20 20"/>
                </svg>
            </div>
        </button>
    </div>

    """

# Returns script controlling menu toggle behavior:
def menu_toggle_js():
    return """
    


    """

# Returns the attribution panel (links to Wellington Sculpture Trust website):
def get_attribution():
    return """

    <div id="attribution" style="
        position: fixed;
        bottom: 12px;
        left: 12px;
        z-index: 9999;
        background-color: white;
        padding: 10px 10px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.3);
        font-family: Arial, sans-serif;
        font-size: 18px;
        width: 300px;
    ">
        <div style="font-size: 12px;">Data gathered from the <a href="https://www.sculpture.org.nz/" target="_blank">Wellington Sculpture Trust</a>.</div>
    </div>

    """

# Returns the standard style sheet for sculpture popups. Used by multiple maps.
def get_popup_css():
    return """

    body {
        font-family: 'Raleway', sans-serif;
    }

    .sculpture-popup {
        padding: 8px;
    }

    .sculpture-popup img {
        display: block;
        margin: 0 auto;
        width: 65%;
        height: 65%;
        object-fit: cover;
    }

    .title-and-artist {
        line-height: 30px;
        margin-bottom: -30px;
        text-align: center;
    }

    .title {
        font-size: 30px;
        font-weight: bold;
        margin: 0 0 8px 0;
        color: #fc6909;
    }

    a {
        color: #428bca;
    }

    .artist {
        font-size: 20px;
        font-weight: bold;
        margin-top: -5px;
        color: #1b3664;
    }

    .details {
        margin-top: 30px;
        margin-bottom: 20px;
        color: #586871;
    }

    .details p {
        margin-top: -10px;
        line-height: 20px;
    }

    .desc {
        padding-top: 15px;
        color: #1b3664;
    }

    """

# Returns html for map marker popups:
def map_marker_html(
        title: str,
        artist: str,
        year: str,
        site: str,
        attributes: str,
        image_url: str,
        description: str,
        web_link: str,
        map_link: str
) -> str:
    html = f"""
            <html>
                <head>
                    <link href="https://fonts.googleapis.com/css?family=Raleway:400,300,600,500,900,700,800" rel="stylesheet" type="text/css">
                    <style>
                        {get_popup_css()}
                    </style>
                </head>
                <body>
                    <div class="sculpture-popup">
                        <div class="popup-desktop">
                            <div class="title-and-artist">
                                <p class="title">{title}</p>
                                <p class="artist">{artist}</p> <br>
                            </div>
                            <img src="{image_url}" alt="{artist} - {title}">
                        </div>
                        <p class="desc">{description}</p>
                        <div class="details">
                                <p>{year}</p>
                                <p>{site}</p>
                                <p>{attributes}</p>
                        </div>
                        <style>
                            {elements.remove_underline()}
                        </style>
                        <div class="icon-links">
                            <a href="{web_link}" target="_blank">
                                <svg xmlns="http://www.w3.org/2000/svg"
                                    width="24" height="24" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2"
                                    stroke-linecap="round" stroke-linejoin="round"
                                    class="lucide lucide-square-arrow-out-up-right-icon lucide-square-arrow-out-up-right">
                                    <path d="M21 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6"></path>
                                    <path d="m21 3-9 9"></path>
                                    <path d="M15 3h6v6"></path>
                                </svg>
                                </a><a href="{map_link}" target="_blank">
                                <svg xmlns="http://www.w3.org/2000/svg"
                                    width="24" height="24" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2"
                                    stroke-linecap="round" stroke-linejoin="round"
                                    class="lucide lucide-map-icon lucide-map">
                                    <path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"></path>
                                    <path d="M15 5.764v15"></path>
                                    <path d="M9 3.236v15"></path>
                                </svg>
                            </a>
                        </div>
                    </div>
                </body>
            </html>
        """
    return html

# Returns a mini version of a webpage embedded on the left side of the map:
def web_frame_html(page: str):
    return f"""
        <div style="{web_frame_css()}" id="web-panel">
            <iframe 
                src="{page}"
                style="
                    width: 100%;
                    height: 470px;
                    border: none;
                "
            ></iframe>
        </div>
    """

# Returns CSS for embedded webapge:
def web_frame_css():
    return """
        position: fixed;
        width: 300px;
        height: 470px;
        left: 12px;
        bottom: 60px;
        z-index: 500;
        border-radius: 5px;
        background: white;
        box-shadow: 0 0 5px rgba(0,0,0,0.3);
    """

# Returns navigation bar element. Used on all maps.
def nav_bar():
    return """
        <div id="navigation" style="
            position: fixed;
            top: 12px;
            right: 12px;
            z-index: 9999;
            background-color: white;
            padding: 10px 10px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.3);
            font-family: Arial, sans-serif;
            font-size: 18px;
        ">
            <div style="font-size: 12px;">
                <span style="color: #FFFFFF;">&#9679;</span> <a href="index.html">All Sculptures</a><br>
                <span style="color: #72b127;">&#9679;</span> <a href="wellington_city_walk.html">Wellington City Walk</a><br>
                <span style="color: #446979;">&#9679;</span> <a href="botanic_garden_walk.html">Botanic Garden Walk</a><br>
                <span style="color: #ff8e7f;">&#9679;</span> <a href="meridian_energy_wind_sculpture_walk.html">Meridian Energy Wind Sculpture Walk</a><br>
            </div>
        </div>
    """