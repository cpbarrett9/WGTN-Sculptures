import folium
import branca
import pandas as pd
from folium import Element
from folium.plugins import Search
import elements

#
#   'all_sculptures': Map of all sculptures commissioned by the Wellington Sculpture Trust.
#   Markers are color-coded by the collection/art walk they belong to.
#

map_name = "all_sculptures"

# Reading data and creating map object:
dataframe = pd.read_csv("WGTN-Sculptures/data/sculpture_database.csv")
m = folium.Map(
        location=[-41.296, 174.78], 
        zoom_start=14,
        tiles='CartoDB Positron'
    )

# Creating and adding legend to map:
legend = elements.get_legend()
m.get_root().html.add_child(Element(legend))

# Creating and adding attribution to map:
attribution = elements.get_attribution()
m.get_root().html.add_child(Element(attribution))

# Creating an adding navigation bar to page:
nav = elements.nav_bar()
m.get_root().html.add_child(Element(nav))

# CSS Styling for map marker popups:
css = elements.get_popup_css()

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
                    <a href="{web_link}" target="_blank">Website</a>
                    <a href="{map_link}" target="_blank">Google Maps</a>
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

# Export map to html file:
m.save(f"{map_name}.html")