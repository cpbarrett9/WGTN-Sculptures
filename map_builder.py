from typing import Sequence
import folium
from pathlib import Path
import pandas as pd
import elements
import branca
from folium import Element
from folium.plugins import LocateControl
from folium.plugins import Search
from folium.plugins import Fullscreen

#
#   'map_builder': Contains functions that return sculpture maps based on specifications.
#

# Returns a folium map of the given sculpture collection:
def build_map(map_name: str, location: Sequence[float], zoom_start:int) -> folium.Map:

    # Creating map object:
    m = folium.Map(
            location=location,
            zoom_start=zoom_start,
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
    hide_menu_toggle = elements.hide_menu_toggle()
    m.get_root().html.add_child(Element(hide_menu_toggle))

    # Creating and adding fullscreen toggle:
    full_screen_button = elements.full_screen_button()
    m.get_root().html.add_child(Element(full_screen_button))

    # Creating an adding navigation bar to page:
    nav = elements.nav_bar()
    m.get_root().html.add_child(Element(nav))

    # Getting correct CSV path:
    BASE_DIR = Path(__file__).resolve().parent
    CSV_PATH = BASE_DIR / "data" / "sculpture_database.csv"

    # Creating dataframe from CSV:
    dataframe = pd.read_csv(CSV_PATH)

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

        # If this isn't an all sculptures map and the marker doesn't match target collection, skip:
        if map_name != "all_sculptures" and collection != map_name:
            continue 

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
            case "botanic_garden_walk":
                marker_color = 'cadetblue'
            case "meridian_energy_wind_sculpture_walk":
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

    # AntPath:
    if map_name != "all_sculptures":
        get_ant_path(map_name).add_to(m)

    return m

# Returns the ant path (representation of suggested walking path) object for each sculpture collection:
def get_ant_path(map_name: str):

    path_points = None
    color = None

    match map_name:

        case "botanic_garden_walk":
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
            color = "blue"

        case "meridian_energy_wind_sculpture_walk":
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
            color = "orange"

        case _:
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
            color = "green"

    return folium.plugins.AntPath(
            locations=path_points,
            opacity=0.5,
            color=color,
            delay=6000
        )