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

    # Fetch the OSM data
    graph = ox.graph_from_place(location, network_type="drive")
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



def display_map_from_df(df):
    # Create a Folium map
    m = folium.Map()

    # Add markers for each place in the DataFrame
    for index, row in df.iterrows():
        popup = f"Place ID: {row['ID']}<br>Name: {row['Place Name']}"
        folium.Marker(location=[row['Latitude'], row['Longitude']], popup=popup).add_to(m)

    return m



def main():
    global graph 
    global map 
    global df
    graph = get_map_data()
    #csv_file = create_csv(graph) already created 

    df=pd.read_csv("nodes_subset_info.csv")

    st.title("Shortest Path Finder")
    map_figure = display_map_from_df(df) 


    st.markdown("<h1 style='text-align: center;'>Map</h1>", unsafe_allow_html=True)
    st.markdown(map_figure._repr_html_(), unsafe_allow_html=True)



main()


