from pathlib import Path
import folium
import pandas as pd
from all_sculptures import build_map

#
#   'test': Takes a map object from all_sculptures and tests if the map generates as expected
#

m = build_map()
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "sculpture_database.csv"
df = pd.read_csv(CSV_PATH)
html = m.get_root().render()

def test_for_folium_map_object():
    assert isinstance(m, folium.Map)

def test_if_markers_match_row_count():
    rows = len(df)
    assert rows == 30

def test_for_green_markers():
    assert "green" in html

def test_for_blue_markers():
    assert "cadetblue" in html

def test_for_red_markers():
    assert "lightred" in html

def test_for_nav():
    assert "https://www.sculpture.org.nz/" in html