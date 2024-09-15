import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd

# Function to get the district boundary
def get_district_boundary(district_name):
    # Use OSMnx to geocode the district name
    gdf = ox.geocode_to_gdf(district_name)
    if not gdf.empty:
        # Extract the geometry of the first result
        admin_poly = gdf.geometry.to_list()[0]
        return admin_poly
    else:
        st.error("District not found.")
        return None

# Function to get building footprints and amenities
def get_buildings_and_amenities(admin_poly):
    # Get building footprints within the district boundary
    footprints = ox.features_from_polygon(admin_poly, tags={'building': True})
    amenities = ox.features_from_polygon(admin_poly, tags={'amenity': True})
    return footprints, amenities

# Streamlit app
st.title('Bratislava District Viewer')

# List of districts
districts = [
    'Staré Mesto, Bratislava',
    'Ružinov, Bratislava',
    'Nové Mesto, Bratislava',
    'Karlova Ves, Bratislava',
    'Dúbravka, Bratislava'
]

# Dropdown menu to select district
selected_district = st.selectbox('Select a district:', districts)

# Get the boundary for the selected district
district_boundary = get_district_boundary(selected_district)

if district_boundary:
    # Get buildings and amenities
    buildings, amenities = get_buildings_and_amenities(district_boundary)

    # Create a plot
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    crs = 23700

    # Plot buildings
    if not buildings.empty:
        buildings = buildings.to_crs(crs)
        buildings.plot(ax=ax, color='grey', alpha=0.5, linewidth=1, edgecolor='k')

    # Plot amenities
    if not amenities.empty:
        amenities = amenities.to_crs(crs)
        amenities.plot(column='amenity', ax=ax, cmap='tab10', alpha=0.5, linewidth=1.5, edgecolor='k', legend=True)

    ax.set_title(f'Buildings and Amenities in {selected_district}')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.axis('off')

    # Display the plot in Streamlit
    st.pyplot(fig)
