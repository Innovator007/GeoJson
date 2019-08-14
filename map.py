import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elev):
	if elev < 1000:
		return "green"
	elif elev>=1000 and elev<3000:
		return "orange"
	else:
		return "red"


map = folium.Map(location=[38.58,-99.09],zoom_start=5)
fgp = folium.FeatureGroup(name="Points")
for lt,ln,el, name in zip(lat,lon,elev,name):
	iframe = folium.IFrame(html=html % (name, name, el), width=200, height=70)
	fgp.add_child(folium.Marker(location=[lt,ln],popup=folium.Popup(iframe),icon=folium.Icon(color=color_producer(el))))
fgg = folium.FeatureGroup(name="Population")
fgg.add_child(folium.GeoJson(data=open("geojson.json","r",encoding="utf-8-sig").read(),
	style_function=lambda x: {"fillColor": "green" if x["properties"]["POP2005"] < 10000000 else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))

map.add_child(fgp)
map.add_child(fgg)
map.add_child(folium.LayerControl())
map.save("advanced_map.html")