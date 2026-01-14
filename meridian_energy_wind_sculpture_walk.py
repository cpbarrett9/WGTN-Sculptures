from pathlib import Path
import folium
import branca
import pandas as pd
from folium import Element
from folium.plugins import Search
import elements
from folium.plugins import LocateControl

#
#   'meridian_energy_wind_sculpture_walk': Map of sculptures specific to the Wind sculpture collection.
#   Includes a the suggested path + live location of the user.
#

map_name = "meridian_energy_wind_sculpture_walk"

# Getting correct CSV path:
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "sculpture_database.csv"

# Reading data and creating map object:
dataframe = pd.read_csv(CSV_PATH)
m = folium.Map(
        location=[-41.3150, 174.8021], 
        zoom_start=16,
        tiles='CartoDB Positron'
    )

# Creating an adding navigation bar to page:
nav = elements.nav_bar()
m.get_root().html.add_child(Element(nav))

# Creating and adding Wellington Sculpture Trust web page as iframe:
info_page_html = elements.web_frame_html("https://www.sculpture.org.nz/walks/the-meridian-energy-wind-sculpture-walk#content-wrap")
m.get_root().html.add_child(Element(info_page_html))

# Creating and adding attribution panel:
attribution = elements.get_attribution()
m.get_root().html.add_child(Element(attribution))

# CSS Styling for map marker popups:
css = elements.get_popup_css()

# Global CSS:
global_css = elements.global_css()
m.get_root().html.add_child(Element(global_css))

# Live location:
LocateControl(
    auto_start=True,
    setView=False
).add_to(m)

# Feature Group for map markers:
fg = folium.FeatureGroup(name="Sculptures").add_to(m)

# Creating map marker from each row of data:
for _, row in dataframe.iterrows():

    # Only turn botanic garden sculptures into markers:
    collection = row['collection']
    if collection != "The Meridian Energy Wind Sculpture Walk":
        continue
    else:

        # Grabbing information for popup display:
        title = row['title']
        artist = row['artist']
        year = row['year']
        site = row['site']
        attributes = row['attributes']
        description = row['description']
        image_url = row['image']
        web_link = row['web_link']
        map_link = row['map_link']

        # Creating html display when marker is clicked:
        html = elements.map_marker_html(
            title=title,
            artist=artist,
            year=year,
            site=site,
            attributes=attributes,
            image_url=image_url,
            description=description,
            web_link=web_link,
            map_link=map_link
        )
        
        # Creating iframe + popup
        iframe = branca.element.IFrame(
            html=html,
            width=550,
            height=400
        )
        popup = folium.Popup(iframe, max_width=550)

        # Determining color of marker:
        marker_color = 'green'  # Default color (Wellington city walk)
        match collection:
            case "Botanic Garden Walk":
                marker_color = 'cadetblue'
            case "The Meridian Energy Wind Sculpture Walk":
                marker_color = 'lightred'
            case _:
                pass
        
        # Create marker and add to feature group:
        folium.Marker(
            icon=folium.Icon(color=marker_color, icon='eye-open'),
            location=[row["y"], row["x"]],
            popup=popup,
            title=title,
            tooltip=title
        ).add_to(fg)

# Sculptures search bar:
Search(
    layer=fg,
    search_label="title",
    placeholder="Search sculptures",
    collapsed=False
).add_to(m)

# Ant path:
# (Points selected with https://geojson.io)
path_points = [
    [-41.31225268949123, 174.79601665467214],
    [-41.312682272627356, 174.79732390738496],
    [-41.31378690197965, 174.79887626998237],
    [-41.31525971199891, 174.8010414072886],
    [-41.3167785124772, 174.80312484130008],
    [-41.316747829989396, 174.80414613248325],
    [-41.31696260710072, 174.80477933301592],
    [-41.31654839346751, 174.8086193878595],
    [-41.316318273645344, 174.8088440719203],
]


folium.plugins.AntPath(
    locations=path_points,
    opacity=0.5,
    color="orange",
    delay=6000
).add_to(m)

# Export map to html file:
m.save(f"{map_name}.html")