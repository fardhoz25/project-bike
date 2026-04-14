import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# CONFIG
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# LOAD DATA (HASIL CLEANING)

day_df = pd.read_csv('dashboard/main_data.csv')
hour_df = pd.read_csv('dashboard/hour_data.csv')

day_df['dteday'] = pd.to_datetime(day_df['dteday'])



st.title("Bike Sharing Dashboard")
st.markdown("""
Dashboard ini menampilkan analisis:
- Pengaruh kondisi cuaca terhadap penyewaan sepeda  
- Pola penyewaan sepeda berdasarkan waktu  

Gunakan filter di sidebar untuk mengeksplorasi data.
""")

# SIDEBAR FILTER (INTERAKTIF)
st.sidebar.header("Filter Data")

# Filter tanggal
start_date = st.sidebar.date_input("Start Date", day_df['dteday'].min())
end_date = st.sidebar.date_input("End Date", day_df['dteday'].max())

# Filter season
season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=day_df['season'].unique(),
    default=day_df['season'].unique()
)

# Filter cuaca
weather_filter = st.sidebar.multiselect(
    "Pilih Cuaca",
    options=day_df['weathersit'].unique(),
    default=day_df['weathersit'].unique()
)

# FILTER DATA
filtered_day = day_df[
    (day_df['season'].isin(season_filter)) &
    (day_df['weathersit'].isin(weather_filter)) &
    (day_df['dteday'] >= pd.to_datetime(start_date)) &
    (day_df['dteday'] <= pd.to_datetime(end_date))
]

# METRIC
st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(filtered_day['cnt'].sum()))
col2.metric("Rata-rata Harian", int(filtered_day['cnt'].mean()))
col3.metric("Jumlah Hari", filtered_day.shape[0])

# VISUALISASI 1
st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

fig1, ax1 = plt.subplots()
sns.barplot(data=filtered_day, x='weathersit', y='cnt', ax=ax1)
ax1.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
ax1.set_xlabel("Kondisi Cuaca")
ax1.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig1)

st.markdown("""
Insight:  
Penyewaan sepeda cenderung lebih tinggi pada kondisi cuaca cerah dan menurun pada kondisi cuaca yang kurang mendukung. Hal ini menunjukkan bahwa faktor cuaca berpengaruh terhadap tingkat penggunaan sepeda.
""")

# VISUALISASI 2
st.subheader("Pola Penyewaan Sepeda per Jam")

fig2, ax2 = plt.subplots()
sns.lineplot(data=hour_df, x='hr', y='cnt', hue='workingday', ax=ax2)
ax2.set_title("Pola Penyewaan per Jam")
ax2.set_xlabel("Jam")
ax2.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig2)

st.markdown("""
Insight:  
Penyewaan sepeda meningkat pada pagi dan sore hari, terutama pada hari kerja. Hal ini menunjukkan pola penggunaan untuk aktivitas mobilitas harian.
""")