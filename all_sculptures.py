import folium
import branca
import pandas as pd
from folium import Element
from folium.plugins import Search
import elements
from folium.plugins import LocateControl
from pathlib import Path

#
#   'all_sculptures': Map of all sculptures commissioned by the Wellington Sculpture Trust.
#   Markers are color-coded by the collection/art walk they belong to.
#

map_name = "all_sculptures"

# Getting correct CSV path:
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "sculpture_database.csv"

def build_map() -> folium.Map:
    # Reading data and creating map object:
    dataframe = pd.read_csv(CSV_PATH)
    m = folium.Map(
            location=[-41.296, 174.78], 
            zoom_start=14,
            tiles='CartoDB Positron',
            attributionControl=False
        )

    # Creating and adding Wellington Sculpture Trust web page as iframe:
    web_page_html = elements.web_frame_html("https://www.sculpture.org.nz/about-the-trust/overview#content-wrap")
    m.get_root().html.add_child(Element(web_page_html))

    # Live location:
    LocateControl(
        auto_start=False,
        setView=False
    ).add_to(m)

    # Global CSS:
    global_css = elements.global_css()
    m.get_root().html.add_child(Element(global_css))

    # Creating and adding attribution to map:
    attribution = elements.get_attribution()
    m.get_root().html.add_child(Element(attribution))

    # Creating and adding menu visibility toggle:
    hide_menu_toggle = elements.hide_menu_toggle();
    m.get_root().html.add_child(Element(hide_menu_toggle))

    # Creating an adding navigation bar to page:
    nav = elements.nav_bar()
    m.get_root().html.add_child(Element(nav))

    # Feature Group for map markers:
    fg = folium.FeatureGroup(name="Sculptures").add_to(m)

    # Creating map marker from each row of data:
    for _, row in dataframe.iterrows():

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
        collection = row['collection']

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

    return m

m = build_map()

# Export map to html file:
m.save(f"index.html")