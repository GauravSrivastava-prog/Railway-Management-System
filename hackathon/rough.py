import folium

# Create a map centered around a specific location
mymap = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

# Add markers to the map
folium.Marker(location=[51.5074, -0.1278], popup='London').add_to(mymap)
folium.Marker(location=[40.7128, -74.0060], popup='New York City').add_to(mymap)
folium.Marker(location=[30.390655, 77.969268], popup="Raghav bhai ka aaya phone roda ho gya rajiv chowk").add_to(mymap)

# Save the map to an HTML file
mymap.save('interactive_map.html')
