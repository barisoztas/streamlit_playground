import streamlit as st
import pandas as pd

data = pd.read_csv(r"./data/grid-access-cm-2_stations.csv")

st.map(data)