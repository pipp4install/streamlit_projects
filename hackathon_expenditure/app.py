import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
import plotly.express as px

# Set Streamlit header styles
st.markdown('<style>h1{color: green; text-align:center;}</style>', unsafe_allow_html=True)
st.markdown('<style>h2{color: black; text-align:center;}</style>', unsafe_allow_html=True)
st.markdown('<style>h3{color: black; text-align:center;}</style>', unsafe_allow_html=True)

st.title("App to find your next mountain walk.")

# Cache to improve app performance
@st.cache
def load_data(url):
    """
    Function to import csv data from GitHub repo.
    Args:
        url (Str): The raw URL of the GitHub page to webscrape.
    Returns:
        df (DataFrame): Pandas DataFrame.
    """
    df = pd.read_csv(url, index_col=[0])
    df = df[["Name", "Metres", "County", "Latitude", "Longitude"]]
    df.rename(columns = {"Metres": "Height (m)", "County": "Section"}, inplace = True)
    return df

url = "https://raw.githubusercontent.com/pippinstall/streamlit_projects/main/hackathon_expenditure/per_capita.csv"
hills = load_data(url)

def create_app(df):
    """
    Function that displays information about selected mountains of interest.
        Args: 
            df (DataFrame): Pandas DataFrame of selected moutains.
        Returns:
            
    """
    # Height filter
    heights = st.sidebar.slider('Select a height (m)', 
                                int(df['Height (m)'].min()),
                                int(df['Height (m)'].max()), 
                                (int(df['Height (m)'].min()),
                                 int(df['Height (m)'].max()))
                               )
    # Section filter
    section = df['Section'].unique()
    filter_section = st.sidebar.multiselect("Select a geographical area:", section)
    
    if filter_section == []:
        selected = df[(df['Height (m)'] >= heights[0]) & (df['Height (m)'] <= heights[1])]
    elif filter_section != []:
        selected = df[(df['Height (m)'] >= heights[0]) & (df['Height (m)'] <= heights[1]) & (df['Section'].isin(filter_section))]
    
    # Exclude
    names = selected['Name'].unique()
    names = sorted(names, reverse = False)
    options = st.sidebar.multiselect("Select mountains to exclude:", names)
    
    if options == []:
        selected = selected
    elif options != [] and filter_section == []:
        selected = df[(df['Height (m)'] >= heights[0]) & (df['Height (m)'] <= heights[1]) & (~df['Name'].isin(options))]
    elif options != [] and filter_section != []:
        selected = df[(df['Height (m)'] >= heights[0]) & (df['Height (m)'] <= heights[1]) & (df['Section'].isin(filter_section)) & (~df['Name'].isin(options))]
    
    
    # Main body
    st.header("View and filter on a map:")
    st.write("The shade size of the dot represents the height of the mountain")
    
    fig = px.scatter_mapbox(selected,
                            lat = "Latitude",
                            lon = "Longitude",
                            hover_name = "Name",
                            hover_data = ["Height (m)"],
                            zoom = 8,
                            height = 300,
                            color = 'Height (m)',
                            size = 'Height (m)',
                            color_continuous_scale = px.colors.diverging.Portland, # https://plotly.com/python/builtin-colorscales/
                            size_max = 9)
    fig.update_layout(mapbox_style = "stamen-terrain") # open-street-map # stamen-terrain
    fig.update_layout(margin = {"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig, use_container_width = True)
    
    st.header("View and filter table:")
    cm = sns.light_palette("seagreen", as_cmap=True)
    st.dataframe(selected.style.background_gradient(cmap=cm))

create_app(hills)
