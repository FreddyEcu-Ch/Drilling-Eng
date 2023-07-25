# Import Python libraries

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image

# Insert an icon
icon = Image.open("Resources/well.jpg")

# state the design of the app
st.set_page_config(page_title="DE App", page_icon=icon)

# Insert css codes to improve the design of the app
st.markdown(
    """
<style>
h1 {text-align: center;
}
body {background-color: #DCE3D5;
      width: 1400px;
      margin: 15px auto;
}
</style>""",
    unsafe_allow_html=True,
)

# Insert title of the app
st.title("Drilling Engineering App ®")

st.write("---")

# Add information of the app
st.markdown(""" This app is used to see 3D wells, as well as,
calculate basic information about their directional trajectories.

***Python:*** Pandas, NumPy, Streamlit, PIL, Plotly.
""")

# Add additional information
expander = st.expander("Information")
expander.write("This is an open-source web app fully programmed in Python for calculating"
               " drilling parameters.")

# Insert image
image = Image.open("Resources/dd.jpg")
st.image(image, width=100, use_column_width=True)

# Insert subheader
st.subheader("**Drilling Fundamentals**")

# Insert video
video = open("Resources/drilling.mp4", "rb")
st.video(video)

# Insert caption
st.caption("*Video about Drilling Engineering*")

# Sidebar section
logo = Image.open("Resources/ESPOL.png")
st.sidebar.image(logo)

# Add title to the sidebar section
st.sidebar.title("⬇ Navigation")

# Upload files
file = st.sidebar.file_uploader("Upload your csv file")

# Add sections of the app
with st.sidebar:
    options = option_menu(
        menu_title="Menu",
        options=["Home", "Data", "3D Plots", "Basic Calculations"],
        icons=["house", "tv-fill", "box", "calculator"],
    )