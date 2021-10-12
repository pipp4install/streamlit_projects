import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
import plotly.express as px


# Set Streamlit header styles
st.markdown('<style>h1{color: green; text-align:center;}</style>', unsafe_allow_html=True)
st.markdown('<style>h2{color: white; text-align:center;}</style>', unsafe_allow_html=True)

st.title("Revenue outturn expenditure, by authority and service in Wales (2019-2020)")


# Cache to improve app performance
@st.cache
def load_data(url):
    """Function to import csv data from GitHub repo."""
    return pd.read_csv(url, index_col=[0])


def create_app(df):
    """Displays information about selected features."""
#     authority = st.selectbox('Select authority:', df['Authority'])
    st.dataframe(df)

#     st.header("View and filter table:")
#     cm = sns.light_palette("seagreen", as_cmap=True)
#     st.dataframe(df.style.background_gradient(cmap=cm))

#     # Main body
#     st.header("View and filter on a map:")
#     st.write("The shade size of the dot represents the expenditure")

#     fig = px.scatter_mapbox(authority,
#                             lat = "Coorindates N",
#                             lon = "Coorindates W",
#                             hover_name = "Authority",
#                             hover_data = service,
#                             zoom = 8,
#                             height = 300,
#                             color = service,
#                             size = service,
#                             color_continuous_scale = px.colors.diverging.Portland, # https://plotly.com/python/builtin-colorscales/
#                             size_max = 9)
#     fig.update_layout(mapbox_style = "stamen-terrain") # open-street-map # stamen-terrain
#     fig.update_layout(margin = {"r":0,"t":0,"l":0,"b":0})

#     st.plotly_chart(fig, use_container_width = True)
    
#     st.header("View and filter table:")
#     cm = sns.light_palette("seagreen", as_cmap=True)
#     st.dataframe(selected.style.background_gradient(cmap=cm))


per_capita = load_data("https://raw.githubusercontent.com/pippinstall/streamlit_projects/main/hackathon_expenditure/per_capita.csv")
total = load_data("https://raw.githubusercontent.com/pippinstall/streamlit_projects/main/hackathon_expenditure/total.csv")

create_app(per_capita)
