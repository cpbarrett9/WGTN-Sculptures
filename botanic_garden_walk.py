from pathlib import Path
import folium
import branca
import pandas as pd
from folium import Element
from folium.plugins import Search
import elements
from folium.plugins import LocateControl

#
#   'botanic_garden_walk': Map of sculptures specific to the Botanic Garden Walk sculpture collection.
#   Includes a the suggested path + live location of the user.
#

map_name = "botanic_garden_walk"

# Getting correct CSV path:
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "sculpture_database.csv"

# Reading data and creating map object:
dataframe = pd.read_csv(CSV_PATH)
m = folium.Map(
        location=[-41.2825, 174.768], 
        zoom_start=17,
        tiles='CartoDB Positron'
    )

# Creating an adding navigation bar to page:
nav = elements.nav_bar()
m.get_root().html.add_child(Element(nav))

# Creating and adding Wellington Sculpture Trust web page as iframe:
garden_walk_page_html = elements.web_frame_html("https://www.sculpture.org.nz/walks/botanic-garden-walk#content-wrap")
m.get_root().html.add_child(Element(garden_walk_page_html))

# Creating and adding attribution panel:
attribution = elements.get_attribution()
m.get_root().html.add_child(Element(attribution))

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
    if collection != "Botanic Garden Walk":
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
    [-41.285238007589314, 174.76775784695553],
    [-41.28511498597266, 174.7676961739051],
    [-41.28507808755543, 174.76779972431916],
    [-41.28481860064743, 174.76800621828005],
    [-41.28466015956139, 174.76817016472086],
    [-41.28462014426564, 174.76840627961565],
    [-41.28451952259906, 174.7685588296677],
    [-41.28433016342333, 174.76860037195195],
    [-41.28417390895686, 174.76860010016662],
    [-41.28406750933024, 174.7687706662702],
    [-41.283985273388176, 174.76888123471548],
    [-41.28360368651219, 174.76905770937134],
    [-41.28321005410076, 174.76921346407272],
    [-41.2829668378014, 174.76929144382166],
    [-41.28285632542839, 174.7692984677907],
    [-41.28278087689735, 174.76941769618702],
    [-41.28277172742289, 174.76963085032617],
    [-41.282674258511825, 174.76978709651638],
    [-41.28248215352705, 174.76990085614563],
    [-41.28210187848301, 174.77000005114473],
    [-41.28194749659332, 174.770054196574],
    [-41.28182383089425, 174.7701708056931],
    [-41.28176084079845, 174.77028810543948],
    [-41.281626683416505, 174.77034248107958],
    [-41.281267666803814, 174.77028042154132],
    [-41.28108018635671, 174.77015820041458],
    [-41.28089508507284, 174.77014988215603],
    [-41.280780221135466, 174.77010716538422],
    [-41.28066159328646, 174.77016585874253],
    [-41.280567819581755, 174.76998880155577],
    [-41.28072759079257, 174.76982291211738],
    [-41.280562994797094, 174.7695291025728],
    [-41.28048046982159, 174.76953851561177],
    [-41.280446853916395, 174.76944289142983],
    [-41.28047681374639, 174.76938111837086],
    [-41.28024463911305, 174.76894988871408],
    [-41.28000391435835, 174.76911474488747],
    [-41.27994375589033, 174.7690333118827],
    [-41.280174113155255, 174.76877919568113],
    [-41.27994334452931, 174.76885524688578],
    [-41.28002204108116, 174.76871535073343],
    [-41.28002742719761, 174.76860360672435],
    [-41.280315562622896, 174.7683170206597],
    [-41.28034024406692, 174.76810818423883],
    [-41.280507435627385, 174.76799828191122],
    [-41.280720010376626, 174.76808973161377],
    [-41.28062792446799, 174.76813423379502],
    [-41.281117685612244, 174.76818949957504],
    [-41.28121308086733, 174.76835622288291],
    [-41.281258983105104, 174.76847683254073],
    [-41.28132597570921, 174.7684631017836],
    [-41.28138427221335, 174.7683498895446],
    [-41.28137047081538, 174.76807643057657],
    [-41.281672601869346, 174.76799243589477],
    [-41.28178183991417, 174.76794191755442],
    [-41.28158207428139, 174.76779471095188],
    [-41.281621010230715, 174.76754669787965],
    [-41.281555986256286, 174.76749626650798],
    [-41.28147132120889, 174.76759675579996],
    [-41.281552914588985, 174.76749002013992],
    [-41.281621010230715, 174.76754669787965],
    [-41.28158369661268, 174.76778437707304],
    [-41.28176938028922, 174.76794384620268],
    [-41.28145122655739, 174.76806031208127],
    [-41.281746494709154, 174.76811543462065],
    [-41.28183933638185, 174.7681951691864],
    [-41.281937110247206, 174.76847579536235],
    [-41.2820102454471, 174.76847455734315],
    [-41.28207451162929, 174.76840075196617],
    [-41.282502390884574, 174.76831362616548],
    [-41.28273390779376, 174.76836181170614],
    [-41.282827786025784, 174.76828006152186],
    [-41.28282847800191, 174.76817240502362],
    [-41.28317757928381, 174.7683233819542],
    [-41.28363353403621, 174.76830993767805],
    [-41.28373842093847, 174.76820967859686],
    [-41.28378159582054, 174.768270213635],
    [-41.28396552026515, 174.76797623015142],
    [-41.284190131581084, 174.7678876862089],
    [-41.28429339532477, 174.7677977610066],
    [-41.28427779928819, 174.7675615500416],
    [-41.284359735138, 174.76740098613152],
    [-41.284622652652324, 174.7674039788618],
    [-41.28479690656762, 174.7674038918916],
    [-41.28496073457969, 174.7675734646893],
    [-41.28503624594176, 174.76768612953816],
    [-41.28523182622974, 174.7677566812756],
]

folium.plugins.AntPath(
    locations=path_points,
    opacity=0.5,
    delay=6000
).add_to(m)

# Export map to html file:
m.save(f"{map_name}.html")