import os
import webbrowser
import folium
import osmnx as ox
from geopy.geocoders import Nominatim
from astar import astar_path

def main() -> None:
    place_name = "Belfast, UK"
    print(f"Downloading map data for {place_name}...")
    graph = ox.graph_from_place(place_name, network_type='drive')
    print("Map data downloaded successfully.")

    geolocator = Nominatim(user_agent="geopath_astar_app")

    start_location = None
    while start_location is None:
        start_query = input("Enter the start location in Belfast: ")
        start_address = f"{start_query}, Belfast, UK"
        print(f"\nGeocoding '{start_address}'...")
        start_location = geolocator.geocode(start_address)
        if start_location is None:
            print("Error, try again. Couldn't find start location.")

    end_location = None
    while end_location is None:
        end_query = input("Enter the end location in Belfast: ")
        end_address = f"{end_query}, Belfast, UK"
        print(f"\nGeocoding '{end_address}'...")
        end_location = geolocator.geocode(end_address)
        if end_location is None:
            print("Error, try again. Couldn't find end location.")

    start_coords = (start_location.latitude, start_location.longitude)
    end_coords = (end_location.latitude, end_location.longitude)

    # find the nearest nodes
    start_node = ox.nearest_nodes(graph, Y=start_coords[0], X=start_coords[1])
    end_node = ox.nearest_nodes(graph, Y=end_coords[0], X=end_coords[1])

    print(f"Start node: {start_node}, End node: {end_node}")

    print("Calculating shortest path with A*...")
    route = astar_path(graph, start_node, end_node)

    if route:
        print(f"Route with {len(route)} nodes found.")

        route_map = folium.Map(location=start_coords, zoom_start=14)

        route_coordinates = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]
        
        folium.PolyLine(
            locations=route_coordinates,
            color="#FF0000",
            weight=5
        ).add_to(route_map)

        folium.Marker(
            location=start_coords,
            popup=f"Start: {start_query}",
            icon=folium.Icon(color="green")
        ).add_to(route_map)

        folium.Marker(
            location=end_coords,
            popup=f"End: {end_query}",
            icon=folium.Icon(color="red")
        ).add_to(route_map)
        
        filepath = "route.html"
        route_map.save(filepath)
        print(f"Map saved to {filepath}")

        absolute_filepath = os.path.abspath(filepath)
        print(f"Opening {absolute_filepath} in browser...")
        webbrowser.open('file://' + absolute_filepath)

    else:
        print("No path found.")

if __name__ == '__main__':
    main()