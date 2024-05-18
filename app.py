import osmnx as ox
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
import csv
from geopy.geocoders import Nominatim
import streamlit as st
import folium


def get_map_data():
    # Define the location (e.g., city name)
    location = "Béjaia, Algeria"
    graph = ox.graph_from_place(location, network_type="drive")

    # Fetch the OSM data"""
    """
    for node_id, data in graph.nodes(data=True):
        # 'node_id' is the unique identifier of the node
        # 'data' is a dictionary containing attributes of the node
        print(f"Node ID: {node_id}")
        print("Node data:")
        print(data)"""
    nodes, edges = ox.graph_to_gdfs(graph)

    nodes_subset = list(graph.nodes())[:40]
    edges_subset = list(graph.edges(nodes_subset))

    sub_graph = nx.Graph()
    sub_graph.add_nodes_from(nodes_subset)
    sub_graph.add_edges_from(edges_subset)
    return sub_graph




def create_csv(sub_graph):
    csv_file = "nodes_subset_info.csv"
    geolocator = Nominatim(user_agent="my_geocoder", timeout=10)  #to find the place_name from latitude and longtitude 
    existing_place_names = set()


    # Open the CSV file in write mode
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["ID", "Place Name", "Latitude", "Longitude"])

        for node_id in sub_graph.nodes:
            node_data = graph.nodes[node_id]
            latitude = node_data["y"]
            longitude = node_data["x"]
            location = geolocator.reverse((latitude, longitude), exactly_one=True)
            place_name = location.address if location else "Unknown"
            

            if place_name not in existing_place_names:
                writer.writerow([node_id, place_name, latitude, longitude])
                existing_place_names.add(place_name) 
    print(f"CSV file '{csv_file}' created successfully with node information.")
    return csv_file


"""
def display_map_from_df(df):
    # Create a Folium map
    m = folium.Map()

    # Add markers for each place in the DataFrame
    for index, row in df.iterrows():
        popup = f"Name: {row['Place Name']}"
        folium.Marker(location=[row['Latitude'], row['Longitude']], popup=popup).add_to(m)

    return m
"""

def a_star_search(g, source, target):
    path = nx.astar_path(g, source, target, weight='length')
    return path


def main():
    global graph 
    global map 
    global df
    graph = get_map_data()
    #csv_file = create_csv(graph) already created 

    df=pd.read_csv("nodes_subset_info.csv")

    st.title("Shortest Path Finder")
    #map_figure = display_map_from_df(df) 

    source = st.selectbox("Select Source Place", df['Place Name'].tolist())
    destination = st.selectbox("Select Destination Place", df['Place Name'].tolist())

    color_list = []
    size_list = []

    for item in df['Place Name'].values:
        if item == source or item == destination:
            color_list.append('#008000')
            size_list.append(50)
        else:
            color_list.append('#FF0000')
            size_list.append(1)

    df['color'] = color_list
    df['size'] = size_list


    if st.button('Find Shortest Path'):
        if source != destination:
            src = df[df['Place Name'] == source]['ID'].values[0]
            dest = df[df['Place Name'] == destination]['ID'].values[0]
            shortest_path = a_star_search(graph, src, dest)
            print(shortest_path)

            """fig, ax = ox.plot_graph_route(
                graph,
                shortest_path,
                route_color='r',
                route_linewidth=3,
                node_size=0,
                figsize=(15, 15),
                show=False,
                close=False
            )
            figure = fig
            st.pyplot(fig=figure)"""










main()


