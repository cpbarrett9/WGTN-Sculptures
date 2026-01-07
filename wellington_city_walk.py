from pathlib import Path
import folium
import branca
import pandas as pd
from folium import Element
from folium.plugins import Search
import elements
from folium.plugins import LocateControl

#
#   'wellington_city_walk': Map of sculptures specific to the Wellington City Walk sculpture collection.
#   Includes a the suggested path + live location of the user.
#

map_name = "wellington_city_walk"

# Getting correct CSV path:
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "sculpture_database.csv"

# Reading data and creating map object:
dataframe = pd.read_csv(CSV_PATH)
m = folium.Map(
        location=[-41.2880, 174.7781], 
        zoom_start=15,
        tiles='CartoDB Positron'
    )

# Creating an adding navigation bar to page:
nav = elements.nav_bar()
m.get_root().html.add_child(Element(nav))

# Creating and adding Wellington Sculpture Trust web page as iframe:
garden_walk_page_html = elements.web_frame_html("https://www.sculpture.org.nz/walks/wellington-city-walk#content-wrap")
m.get_root().html.add_child(Element(garden_walk_page_html))

# Creating and adding attribution panel:
attribution = elements.get_attribution()
m.get_root().html.add_child(Element(attribution))

# Global CSS:
global_css = elements.global_css()
m.get_root().html.add_child(Element(global_css))

# Live location:
LocateControl(
    auto_start=True,
    setView=False
).add_to(m)

# CSS Styling for map marker popups:
css = elements.get_popup_css()

# Feature Group for map markers:
fg = folium.FeatureGroup(name="Sculptures").add_to(m)

# Creating map marker from each row of data:
for _, row in dataframe.iterrows():

    # Only turn botanic garden sculptures into markers:
    collection = row['collection']
    if collection != "Wellington City Walk":
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
        html = f"""
            <html>
                <head>
                    <style>
                        {css}
                    </style>
                </head>
                <body>
                    <div class="sculpture-popup">
                        <div class="columns">
                            <div class="column1">
                                <div class="title-and-artist">
                                    <p class="title">{title}</p>
                                    <p class="artist">{artist}</p> <br>
                                </div>
                                <div class="details">
                                        <p>{year}</p>
                                        <p>{site}</p>
                                        <p>{attributes}</p>
                                </div>
                            </div>
                            <div class="column2">
                                <img src="{image_url}" alt="Sculpture image ({artist} - {title})">
                            </div>
                        </div>
                        <p class="desc">{description}</p>
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
        
        # Creating iframe + popup
        iframe = branca.element.IFrame(
            html=html,
            width=700,
            height=400
        )
        popup = folium.Popup(iframe, max_width=700)

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
    [-41.278914664517686, 174.77863159876915],
    [-41.27905404567252, 174.77813303083173],
    [-41.27957110200752, 174.77724349153675],
    [-41.27895905947915, 174.77692139127169],
    [-41.278853400967584, 174.77672719798784],
    [-41.27871384659253, 174.77554212241688],
    [-41.28186514660243, 174.77499421411756],
    [-41.28200181304509, 174.77515522745068],
    [-41.282086615668554, 174.775873395659],
    [-41.28195028609937, 174.77618719456558],
    [-41.28241495296759, 174.7760227581295],
    [-41.28309857453187, 174.77565525615864],
    [-41.28328222163961, 174.77556893794184],
    [-41.28443544353842, 174.77551602344255],
    [-41.28497420583507, 174.77720359479412],
    [-41.285581929323165, 174.77678451361476],
    [-41.285376297287684, 174.77589168076582],
    [-41.28643843611319, 174.77630043366503],
    [-41.2882066043425, 174.77534742089705],
    [-41.28855175251323, 174.77622021385992],
    [-41.28882963578888, 174.77621660521868],
    [-41.28919261312157, 174.77663261899283],
    [-41.2899260573139, 174.77763908788188],
    [-41.290196903075554, 174.77750182796336],
    [-41.29717860768137, 174.77355524955345],
    [-41.29684900275445, 174.77272009845188],
    [-41.29749774695846, 174.77241948667984],
    [-41.298426560295695, 174.77553757386585],
    [-41.29784585060204, 174.77577847920946],
    [-41.29865069801713, 174.7782930718251],
    [-41.291366130143174, 174.78244212159706],
    [-41.291735542026, 174.78377011767418],
    [-41.28939744541947, 174.7831341432041],
    [-41.28962712405765, 174.78031633928566],
    [-41.288359038801474, 174.7801076405362],
    [-41.28789979487225, 174.77953405392975],
    [-41.28801947902281, 174.77900791500235],
    [-41.287911576195796, 174.77951027533953],
    [-41.2866164542729, 174.77922663988778],
    [-41.283964974336286, 174.77896406317848],
    [-41.28278238034889, 174.7794104659307],
    [-41.28200988790933, 174.77921027708493],
    [-41.280678299936866, 174.78029361221655],
]


folium.plugins.AntPath(
    locations=path_points,
    opacity=0.5,
    color="green",
    delay=6000
).add_to(m)

# Export map to html file:
m.save(f"{map_name}.html")