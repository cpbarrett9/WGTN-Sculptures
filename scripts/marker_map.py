import folium
import branca
import pandas as pd
from folium import Element

# Reading data and creating map object:
dataframe = pd.read_csv("WGTN-Sculptures/data/sculpture_database.csv")
m = folium.Map(
        location=[-41.29, 174.78], 
        zoom_start=14,
        tiles='CartoDB Positron'
    )

# Creating and adding legend to map:
legend_html = """
        <div style="
            position: fixed;
            bottom: 12px;
            left: 12px;
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
            <span style="color: #ff8e7f;">&#9679;</span> The Meridian Energy Wind Sculpture Walk
        </div>
    """
m.get_root().html.add_child(Element(legend_html))

# CSS Styling for map marker popups:
css = """

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

description = """

    Mary-Louise Browne lives in Auckland and has exhibited widely throughout New Zealand. She has developed several public art commissions. 

    Words are the recurring subject of her work as she explores the power of language. Mary-Louise’s works challenge conventional readings and demonstrate how apparently simple words or maxims can have multiple layers of meaning. 

    Although the staircase will be reminiscent of memorials, and there is an obvious allusion to immortality and an afterlife, on this site it is positioned as an invitation to climb and to read.

"""

# details:
year = "2013"
site = "Midland Park, Lambton Quay"
attributes = "Marine grade 316 stainless steel / H 3300mm"

image = "WGTN-Sculptures/images/Woman of Words.jpg"

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

    # Adding marker:
    marker_color = 'green'  # Default color (Wellington city walk)
    match collection:
        case "Botanic Garden Walk":
            marker_color = 'cadetblue'
        case "The Meridian Energy Wind Sculpture Walk":
            marker_color = 'lightred'
    folium.Marker(
        icon=folium.Icon(color=marker_color, icon='eye-open'),
        location=[row["y"], row["x"]],
        popup=popup,
    ).add_to(m)

m.save("wellington_sculptures.html")