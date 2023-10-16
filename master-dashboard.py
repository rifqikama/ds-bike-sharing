import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
# ----------Data Source----------#
day_df = pd.read_csv('https://github.com/halycon77/ds-bike-sharing/blob/67cc1fedbacb565ecc591e15ebe54c1d22ab7274/day.csv')
hour_df = pd.read_csv('https://github.com/halycon77/ds-bike-sharing/blob/67cc1fedbacb565ecc591e15ebe54c1d22ab7274/hour.csv')
# ----------Data Source----------#

# ----------Data Cleaning----------#
hour_df['datetime'] = hour_df['dteday'].astype(
    str) + ' ' + hour_df['hr'].astype(str)+':00:00'
hour_df['dteday'] = hour_df['datetime']
hour_df['dteday'] = pd.to_datetime(hour_df['datetime'])
hour_df.drop(['datetime'], axis=1, inplace=True)
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
# Denormalized value
day_df.yr.replace(0, 2011, inplace=True)
day_df.yr.replace(1, 2012, inplace=True)
hour_df.yr.replace(0, 2011, inplace=True)
hour_df.yr.replace(1, 2012, inplace=True)
day_df['temp'] *= 41
day_df['atemp'] *= 50
day_df['hum'] *= 100
day_df['windspeed'] *= 67
day_df['cnt'] = day_df['casual'] + day_df['registered']
hour_df['temp'] *= 41
hour_df['atemp'] *= 50
hour_df['hum'] *= 100
hour_df['windspeed'] *= 67
hour_df['cnt'] = hour_df['casual'] + hour_df['registered']
# ----------Data Cleaning----------#
hour_df.set_index('dteday', inplace=True)
daily_data = pd.DataFrame()
resampling_feature = {
    'season': 'ffill',
    'yr': 'min',
    'mnth': 'min',
    'weekday': 'min',
    'workingday': 'min',
    # 'weathersit': 'min',
    'temp': 'mean',
    'atemp': 'mean',
    'hum': 'mean',
    'windspeed': 'mean',
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}
for feature, method in resampling_feature.items():
    daily_data[feature] = hour_df[feature].resample('D').agg(method)
daily_data.reset_index(inplace=True)

st.markdown(
    """
    # Bike Sharing Analysis
    - Nama: Rifqi Kamaddin Sholeh Lubis
    - Email: rifqi.kamaddin@gmail.com
    - Id Dicoding: rifqikama177
    ---
    """
)
with st.sidebar:
    st.text('Rentang Waktu')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=datetime.date(2011, 1, 1),
        max_value=datetime.date(2012, 12, 31),
        value=[datetime.date(2011, 1, 1), datetime.date(2012, 12, 31)]
    )
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
filtered_df = daily_data[(daily_data['dteday'] >= start_date) & (
    daily_data['dteday'] <= end_date)]
st.header('Dashboard')
st.write(start_date, ' - ', end_date)
st.subheader('Rent Info')
st.write()
col1, col2, col3 = st.columns(3)
with st.container():
    with col1:
        st.header(filtered_df['cnt'].sum())
        st.write('Total Rent')
    with col2:
        st.header(filtered_df['registered'].sum())
        st.write('Registered user')
    with col3:
        st.header(filtered_df['casual'].sum())
        st.write('Casual user')
col1, col2 = st.columns([1, 5])
filtered_df = daily_data[(daily_data['dteday'] >= start_date) & (
    daily_data['dteday'] <= end_date)]

with st.container():
    with col1:
        casual_check = st.checkbox('Casual', value=True)
    with col2:
        registered_check = st.checkbox('Registered')
    fig, ax = plt.subplots(figsize=(18, 8))
    ax.set_title('Trend Peminjaman Sepeda Januari 2011 s/d Desember 2012')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah')
    filtered_df = daily_data[(daily_data['dteday'] >= start_date) & (
        daily_data['dteday'] <= end_date)]
    if casual_check and registered_check:
        sns.lineplot(
            data=filtered_df, x='dteday', y='casual', marker='', label='Casual')
        sns.lineplot(data=filtered_df, x='dteday',
                     y='registered', marker='', label='Registered')
        sns.lineplot(data=filtered_df, x='dteday',
                     y='cnt', marker='', label='Total')
        ax.legend()
    elif casual_check:
        sns.lineplot(
            data=filtered_df, x='dteday', y='casual', marker='', label='Casual')
        ax.legend()
    elif registered_check:
        sns.lineplot(data=filtered_df, x='dteday',
                     y='registered', marker='', label='Registered')
        ax.legend()
    st.pyplot(fig)
st.caption('Copyright (c) 2023')
