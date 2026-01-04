import folium
import pandas as pd

dataframe = pd.read_json("data/sculpture.json", encoding="latin-1")
m = folium.Map(location=[-41.29, 174.78], zoom_start=14)

for _, row in dataframe.iterrows():
    folium.Marker(
        location=[row["y"], row["x"]],
        popup=f"{row['sculpture']} – {row['artist']}",
    ).add_to(m)

m.save("wellington_sculptures.html")

#this is a comment