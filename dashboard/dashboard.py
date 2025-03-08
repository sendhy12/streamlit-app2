import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='whitegrid')
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Load Data
df = pd.read_csv("main_data.csv")
df['datetime'] = pd.to_datetime(df['datetime'])
df['year'] = df['datetime'].dt.year

# Sidebar Filter
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/7a/USB_YPKP_Logo.png")
    st.markdown("## Rentang Tahun")
    start_year, end_year = st.slider("Pilih Rentang Tahun", int(df['year'].min()), int(df['year'].max()), (int(df['year'].min()), int(df['year'].max())))
    st.markdown("---")
    st.write("### Filter Tambahan")
    cluster_filter = st.multiselect("Pilih Kategori Kualitas Udara", options=df["Cluster"].unique(), default=df["Cluster"].unique())

# Filter Data
main_df = df[(df['year'] >= start_year) & (df['year'] <= end_year) & (df['Cluster'].isin(cluster_filter))]

# Tren PM2.5 dan PM10
pm_trend = main_df.groupby('year')[['PM2.5', 'PM10']].mean()

st.subheader("🌍 Tren PM2.5 dan PM10 dari Tahun ke Tahun")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(pm_trend.index, pm_trend['PM2.5'], marker='o', label='PM2.5', color='red')
ax.plot(pm_trend.index, pm_trend['PM10'], marker='s', label='PM10', color='blue')
ax.set_xlabel("Tahun")
ax.set_ylabel("Konsentrasi (µg/m³)")
ax.set_title("Tren PM2.5 dan PM10 dari Tahun ke Tahun")
ax.legend()
ax.grid()
st.pyplot(fig)

# Korelasi PM2.5 dengan Faktor Cuaca
st.subheader("📈 Korelasi Faktor Cuaca dengan PM2.5")
weather_factors = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM', 'PM2.5']
correlation_matrix = main_df[weather_factors].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title("Korelasi Faktor Cuaca dengan PM2.5")
st.pyplot(fig)

# Distribusi Cluster Kualitas Udara
st.subheader("📊 Distribusi Kategori Kualitas Udara")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x=main_df['Cluster'], palette={'Baik': 'green', 'Sedang': 'orange', 'Buruk': 'red'}, ax=ax)
ax.set_xlabel("Kategori Kualitas Udara")
ax.set_ylabel("Jumlah Data")
ax.set_title("Distribusi Cluster Kualitas Udara")
st.pyplot(fig)

# Tren Perubahan Kualitas Udara dari Waktu ke Waktu
st.subheader("📅 Tren Perubahan Kualitas Udara dari Waktu ke Waktu")
fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(main_df, x='year', hue='Cluster', multiple='stack', palette={'Baik': 'green', 'Sedang': 'orange', 'Buruk': 'red'}, ax=ax)
ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah Data")
ax.set_title("Tren Perubahan Kualitas Udara dari Waktu ke Waktu")
st.pyplot(fig)

# Hubungan Suhu dengan Kategori Kualitas Udara
st.subheader("🌡️ Hubungan Suhu dengan Kategori Kualitas Udara")
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(x=main_df['TEMP'], y=main_df['PM2.5'], hue=main_df['Cluster'], palette={'Baik': 'green', 'Sedang': 'orange', 'Buruk': 'red'}, alpha=0.6, ax=ax)
ax.set_xlabel("Suhu (°C)")
ax.set_ylabel("PM2.5")
ax.set_title("Hubungan Suhu dengan Kategori Kualitas Udara")
st.pyplot(fig)

# Hubungan Kecepatan Angin dengan Kategori Kualitas Udara
st.subheader("💨 Hubungan Kecepatan Angin dengan Kategori Kualitas Udara")
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(x=main_df['WSPM'], y=main_df['PM2.5'], hue=main_df['Cluster'], palette={'Baik': 'green', 'Sedang': 'orange', 'Buruk': 'red'}, alpha=0.6, ax=ax)
ax.set_xlabel("Kecepatan Angin (m/s)")
ax.set_ylabel("PM2.5")
ax.set_title("Hubungan Kecepatan Angin dengan Kategori Kualitas Udara")
st.pyplot(fig)

st.caption("© 2025 Sendhy Maula Ammarulloh.")
