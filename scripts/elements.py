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
# - Sends search bar to top of Z-index so things don't overlap it
# - Styling for icon links at the bottom of popups
def global_css():
    return """
    <style>
        .leaflet-control-search {
            z-index: 10000 !important;
        }
    </style>
    """

def remove_underline():
    return """

            .icon-links a {
            text-decoration: none;
        }

    """

# Returns a legend of colors and their corresponding sculpture collections. Used by 'all_sculptures' map:
def get_legend():
    return """

    <div style="
            position: fixed;
            top: 60px;
            right: 12px;
            z-index: 9999;
            background-color: white;
            padding: 10px 15px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.3);
            font-family: Arial, sans-serif;
            font-size: 18px;
        ">
            <b>Collections:</b><br>
            <span style="color: #72b127;">&#9679;</span> Wellington City Walk<br>
            <span style="color: #446979;">&#9679;</span> Botanic Garden Walk<br>
            <span style="color: #ff8e7f;">&#9679;</span> The Meridian Energy Wind Sculpture Walk<br>
            
    </div>   
    """

# Returns the attribution panel (links to Wellington Sculpture Trust website):
def get_attribution():
    return """

    <div style="
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
        font-family: "Helvetica Neue", Helvetica, sans-serif;
    }

    .sculpture-popup {
        padding: 8px;
    }

    .sculpture-popup img {
        max-width: 380px;
        min-width: 380px;
        max-height: 230px;
        min-height: 230px;
        padding-left: 12px;
        object-fit: cover;
    }

    .title-and-artist {
        padding-top: -40px;
        line-height: 30px;
    }

    .title {
        font-size: 30px;
        font-weight: bold;
        margin: 0 0 8px 0;
    }

    .artist {
        font-size: 20px;
        margin-top: -5px;
    }

    .details {
        margin-top: -35px;
    }

    .details p {
        margin-top: -10px;
        font-style: italic;
        line-height: 20px;
    }

    .columns {
        display: flex;
    }

    .column1 {
        max-width: 275px;
        float: left;
    }

    .column2 {
        max-width: 275px;
        float: right;
        justify-content: right;
    }

    .desc {
        padding-top: 15px;
    }

    """

# Returns a mini version of a webpage embedded on the left side of the map:
def web_frame_html(page: str):
    return f"""
        <div style="{web_frame_css()}">
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
        <div style="
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
                <span style="color: #FFFFFF;">&#9679;</span> <a href="all_sculptures.html">All Sculptures</a><br>
                <span style="color: #72b127;">&#9679;</span> <a href="wellington_city_walk.html">Wellington City Walk</a><br>
                <span style="color: #446979;">&#9679;</span> <a href="botanic_garden_walk.html">Botanic Garden Walk</a><br>
                <span style="color: #ff8e7f;">&#9679;</span> <a href="meridian_energy_wind_sculpture_walk.html">Meridian Energy Wind Sculpture Walk</a><br>
            </div>
        </div>
    """