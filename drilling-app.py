# Import Python libraries

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
from collections import namedtuple
from math import acos, asin, cos, sin, atan, sqrt, radians, degrees

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
footer {
  display: none;
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


# Useful functions
# Function for observing data
def data(dataframe):
    st.subheader("**View dataframe**")
    st.write(dataframe.head())
    st.subheader("**Statistical summary**")
    st.write(dataframe.describe())


# Function to visualize wells in 3D
def plots(dataframe):
    st.subheader("Visualize the 3D trajectory of a well")
    x = st.selectbox("Choose DispNS", dataframe.columns)
    y = st.selectbox("Choose DispEW", dataframe.columns)
    z = st.selectbox("Choose tvd", dataframe.columns)
    fig = px.line_3d(dataframe, x, y, z)
    st.plotly_chart(fig)

# Functions to calculate directional parameters
# Function for J type well

Data = namedtuple("Input", "TVD KOP BUR DH")
Output = namedtuple("Output", "R Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_total")


def well_J(data: Data, unit="ingles") -> Output:
    # Call input values
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dh = data.DH
    if unit == "ingles":
        R = 5729.58 / bur
    else:
        R = 1718.87 / bur
    if dh > R:
        dc = dh - R
    elif dh < R:
        dc = R - dh
    do = tvd - kop
    doc = degrees(atan(dc / do))
    oc = sqrt(dc**2 + do**2)
    boc = degrees(acos(R / oc))
    if R < dh:
        bod = boc - doc
    elif R > dh:
        bod = boc + doc
    theta = 90 - bod
    tvd_eob = kop + abs(R * sin(radians(theta)))
    if unit == "ingles":
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R - R * cos(radians(theta))
    tan_len = sqrt(oc**2 - R**2)
    if unit == "ingles":
        md_total = kop + (theta / bur) * 100 + tan_len
    else:
        md_total = kop + (theta / bur) * 30 + tan_len

    output_J = Output(
        R=R,
        Theta=theta,
        TVD_EOB=tvd_eob,
        Md_EOB=md_eob,
        Dh_EOB=dh_eob,
        Tan_len=tan_len,
        Md_total=md_total,
    )

    names = ["R", "theta", "tvd_EOB", "MD_EOB", "DH_EOB", "Length_tan", "MD_Total"]
    for param, value in zip(names, output_J):
        if unit == "ingles":
            if param == "theta":
                st.success(f"{param} -> {value:.3f} degrees")
            else:
                st.success(f"{param} -> {value:.3f} ft")

        else:
            if param == "theta":
                st.success(f"{param} -> {value:.3f} degrees")
            else:
                st.success(f"{param} -> {value:.3f} m")


# Call data
if file:
    df = pd.read_csv(file)

    if options == "Data":
        data(df)

    elif options == "3D Plots":
        plots(df)

    elif options == "Basic Calculations":
        st.subheader("**Select units**")
        units = st.selectbox("Units", ("ingles", "metric"))
        if st.checkbox("J type well"):
            Data = namedtuple("Input", "TVD KOP BUR DH")
            st.subheader("**Enter input values**")
            kop = st.number_input("Enter kop value: ")
            tvd = st.number_input("Enter tvd value: ")
            dh = st.number_input("Enter dh value: ")
            bur = st.number_input("Enter bur value")
            st.subheader("**Show results**")
            well_J(Data(tvd, kop, bur, dh), units)


