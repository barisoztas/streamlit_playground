import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64


st.title('Deneme')

@st.cache
def load_data(path):
    data = pd.read_csv(path)
    return data

@st.cache
def hourly_to_daily(hourly_df):
    daily_average = hourly_df.groupby(pd.Grouper(freq='M', key='date')).mean()
    return daily_average

@st.cache
def hourly_to_yearly(hourly_df):
    yearly_average = hourly_df.groupby(by=hourly_df['date'].dt.year).mean()
    return yearly_average

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv().encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="yearly.csv" target="_blank">Download csv file</a>'
    return href


input_path = r"/home/baris/PycharmProjects/first_app/data/grid-cnrm_cmip6.csv"
data_load_state = st.text('Loading data...')
data = load_data(input_path)
data_load_state.text("Done! ")

st.subheader('CMIP6 Grid values for each day of 1974-2014 period!')
st.write(data)
filtered_data = data[data['id'] == 0]
filtered_data['date'] = pd.to_datetime(filtered_data['date'], format='%Y-%m-%d %H:%M:%S')
filtered_data_daily = hourly_to_daily(filtered_data)
filtered_data_yearly = hourly_to_yearly(filtered_data)
st.subheader('Hourly')
st.line_chart(filtered_data.rename(columns={'date':'index'}).set_index('index')['cmip6_value']-273.15)
st.subheader('Monthly')
st.line_chart(filtered_data_daily['cmip6_value']-273.15)
st.subheader('Yearly')
st.line_chart(filtered_data_yearly['cmip6_value']-273.15)
st.markdown(get_table_download_link(filtered_data_yearly), unsafe_allow_html=True)
