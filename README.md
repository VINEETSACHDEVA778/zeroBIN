# Smart Waste Collection Optimization

## Overview
This project aims to optimize the waste collection process by determining the most efficient route for garbage collection trucks using Google OR-Tools. The system utilizes location data from waste bins, their fill status, and applies route optimization algorithms to minimize travel distance and time.

## Features
- Real-time bin status tracking (Full/Empty)
- Route optimization using Haversine distance and Google OR-Tools
- Interactive map visualization of optimized waste collection routes using Folium
- Exportable waste collection route map in HTML format

## Technologies Used
- Python for data processing and algorithm implementation
- Google OR-Tools for route optimization
- Folium for map visualization
- Pandas for data handling
- OpenPyXL for Excel file processing

## Installation
### Prerequisites
Ensure you have Python installed along with the necessary dependencies.

pip install --upgrade pip
pip install ortools folium openpyxl pandas
## Usage
1. Prepare the Data: Ensure the content.xlsx file contains bin data with columns:
   - Bin ID (Unique Identifier)
   - Status (Full/Empty)
   - Latitude & Longitude (Geographical Coordinates)

2. Run the Script: Execute the script to process data, optimize routes, and generate a map.
  
   python waste_collection.py
   
3. View the Route Map: After execution, download and open waste_collection_route.html to visualize the optimized route.

## How It Works
1. Reads Bin Data: Loads bin details from an Excel file.
2. Calculates Distance Matrix: Uses the Haversine formula to compute distances between bins.
3. Optimizes Route: Implements Google OR-Tools for Vehicle Routing Problem (VRP) optimization.
4. Visualizes Route: Displays bins and optimized path on a Folium map.
5. Exports Results: Saves the interactive map as waste_collection_route.html for easy sharing.

## Output
- Optimized Waste Collection Route displayed in console.
- Interactive Route Map in waste_collection_route.html.
- Color-coded Bins (Red for full, Green for empty) for easy identification.

## Future Improvements
- Integration with real-time IoT sensors for automatic status updates.
- Support for multiple waste collection vehicles.
- Mobile app integration for real-time tracking.

## License
This project is open-source and available under the MIT License.

## Contributors
- Vineet Kumar
- Raj Verma
- Yashika Chaudhary  
Feel free to contribute, suggest improvements, or report issues!

---
Happy Coding! 🚀
