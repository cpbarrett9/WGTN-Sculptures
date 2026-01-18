import map_builder

#
#   'WGTN_sculptures': Generates HTML files for the website's four pages.
#   See map_builder.py for map generation logic, see elements.py for HTML & CSS elements.
#

# All Sculptures Page:
m = map_builder.build_map(map_name="all_sculptures", 
                          location=[-41.296, 174.78],
                          zoom_start=14
                          )
m.save("index.html") # <- Export map to html file

# Wellington City Walk Page:
map_name = "wellington_city_walk"
m = map_builder.build_map(map_name=map_name, 
                          location=[-41.2880, 174.7781],
                          zoom_start=15
                          )

m.save(f"{map_name}.html") # <- Export map to html file

# Botanic Garden Walk Page:
map_name = "botanic_garden_walk"
m = map_builder.build_map(map_name=map_name, 
                          location=[-41.2825, 174.768],
                          zoom_start=17
                          )
m.save(f"{map_name}.html") # <- Export map to html file

# Wind Walk Page:
map_name = "meridian_energy_wind_sculpture_walk"
m = map_builder.build_map(map_name=map_name, 
                          location=[-41.3150, 174.8021],
                          zoom_start=16
                          )
m.save(f"{map_name}.html") # <- Export map to html file