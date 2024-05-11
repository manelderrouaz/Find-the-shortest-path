import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import csv
from geopy.geocoders import Nominatim

# Define the location (e.g., city name)
location = "Béjaia, Algeria"

# Fetch the OSM data
graph = ox.graph_from_place(location, network_type="drive")
nodes, edges = ox.graph_to_gdfs(graph)

nodes_subset = list(graph.nodes())[:30]
edges_subset = list(graph.edges(nodes_subset))

sub_graph = nx.Graph()
sub_graph.add_nodes_from(nodes_subset)
sub_graph.add_edges_from(edges_subset)




csv_file = "nodes_subset_info.csv"
geolocator = Nominatim(user_agent="my_geocoder", timeout=10)  # Increase timeout to 10 seconds
#to find the place_name from latitude and longtitude 


# Open the CSV file in write mode
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(["ID", "Place Name", "Latitude", "Longitude"])

    for node_id in nodes_subset:
        node_data = graph.nodes[node_id]
        latitude = node_data["y"]
        longitude = node_data["x"]
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        place_name = location.address if location else "Unknown"
        

        writer.writerow([node_id, place_name, latitude, longitude])

print(f"CSV file '{csv_file}' created successfully with node information.")
