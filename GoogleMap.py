# Upgrade pip and install required packages
!pip install --upgrade pip
!pip install ortools folium openpyxl pandas

import pandas as pd

# Load your Excel file
file_path = '/content/data.xlsx'  # Change this to your uploaded file's name
data = pd.read_excel(file_path)

# Display the data to check if it's loaded correctly
data.head()

# Check for missing values
print(data.isnull().sum())

# Convert status to a more usable format (if needed)
data['Status'] = data['Status'].map({'EMPTY': 0, 'FULL': 1})

import math

def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great-circle distance between two points on the Earth specified in decimal degrees."""
    # Convert latitude and longitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import math
import folium

# Step 1: Define the Haversine Function
def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great-circle distance between two points on the Earth specified in decimal degrees."""
    # Convert latitude and longitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

# Step 2: Create Data Model
def create_data_model(data):
    """Stores the data for the problem."""
    data_model = {}
    data_model['distance_matrix'] = create_distance_matrix(data)
    data_model['num_vehicles'] = 1  # Change this if you have multiple trucks
    data_model['depot'] = 0  # Index of the starting point (first bin)
    return data_model

# Step 3: Create Distance Matrix
def create_distance_matrix(data):
    distance_matrix = []
    for i in range(len(data)):
        row = []
        for j in range(len(data)):
            distance = haversine(data['Longitude'][i], data['Latitude'][i],
                                 data['Longitude'][j], data['Latitude'][j])
            row.append(distance)
        distance_matrix.append(row)
    return distance_matrix

# Step 4: Print the Solution
def print_solution(manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    index = routing.Start(0)  # Index of the starting node
    route = []
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    route.append(manager.IndexToNode(index))  # Add the end node
    print(f'Route: {route}')
    print(f'Total distance: {total_distance} km')
    return route

# Step 5: Main Function to Execute Route Optimization
def main(data):
    # Instantiate the data problem.
    data_model = create_data_model(data)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data_model['distance_matrix']), data_model['num_vehicles'], data_model['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        # Returns the distance between the two nodes.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data_model['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set the search parameters.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(manager, routing, solution)
    else:
        print('No solution found!')

# Step 6: Execute the Main Function
# Assuming `data` is your DataFrame with columns ['Bin ID', 'Status', 'Latitude', 'Longitude']
route = main(data)

import folium

# Create a map centered around the first bin's location
map_center = [data['Latitude'][0], data['Longitude'][0]]
mymap = folium.Map(location=map_center, zoom_start=14)

# Add markers for each bin with different colors based on the bin's status
for idx, row in data.iterrows():
    # Choose marker color based on bin status (red for full, green for empty)
    marker_color = 'red' if row['Status'] else 'green'

    # Add marker to the map
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        popup=f"Bin ID: {row['Bin ID']}, Status: {'Full' if row['Status'] else 'Empty'}",
        icon=folium.Icon(color=marker_color)
    ).add_to(mymap)

# Save the map
mymap.save('waste_collection_route.html')

from google.colab import files

files.download('waste_collection_route.html')
