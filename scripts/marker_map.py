import folium
import branca
import pandas as pd
from folium import Element

# Reading data and creating map object:
dataframe = pd.read_json("WGTN-Sculptures/data/sculpture.json", encoding="latin-1")
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
            <b>Legend</b><br>
            <span style="color: DarkOliveGreen;">&#9679;</span> Permanent<br>
            <span style="color: DarkKhaki;">&#9679;</span> Temporary (Current)<br>
            <span style="color: LightCoral;">&#9679;</span> Temporary (Retired)
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

    .title-and-artist {
        line-height: 0.5px;
    }

    .title {
        font-size: 30px;
        font-weight: bold;
    }

    .artist {
        font-size: 20px;
    }

"""

description = """

    Mary-Louise Browne lives in Auckland and has exhibited widely throughout New Zealand. She has developed several public art commissions. 

    Words are the recurring subject of her work as she explores the power of language. Mary-Louise’s works challenge conventional readings and demonstrate how apparently simple words or maxims can have multiple layers of meaning. 

    Although the staircase will be reminiscent of memorials, and there is an obvious allusion to immortality and an afterlife, on this site it is positioned as an invitation to climb and to read.

"""

details = """

    1996<br>
    Granite / 7000 x 1000mm<br>
    Norwood Path, Botanic Garden<br>

"""

for _, row in dataframe.iterrows():

    # Grabbing information for popup display:
    sculpture = row['sculpture']
    artist = row['artist']

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
                    <div class="title-and-artist">
                        <p class="title">{sculpture}</p>
                        <p class="artist">{artist}</p>
                    </div>
                    <p class="desc">{description}</p>
                    <p class="details">{details}</p>
                </div>
            </body>
        </html>
    """
    
    # Creating iframe + popup
    iframe = branca.element.IFrame(
        html=html,
        width=500,
        height=300
    )
    popup = folium.Popup(iframe, max_width=500)

    # Adding marker:
    folium.Marker(
        icon=folium.Icon(color='green', icon='eye-open'),
        location=[row["y"], row["x"]],
        popup=popup,
    ).add_to(m)

m.save("wellington_sculptures.html")