# ----------------------------
# app.py - Enhanced Dashboard
# ----------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from sqlalchemy import create_engine
from io import BytesIO

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="Community Fever & Malaria Dashboard", layout="wide")

# ----------------------------
# Connect to SQLite
# ----------------------------
engine = create_engine("sqlite:///../database/surveillance.db")
df = pd.read_sql("SELECT * FROM surveillance_reports", engine)
df['report_date'] = pd.to_datetime(df['report_date'])
df['week'] = df['report_date'].dt.isocalendar().week

# ----------------------------
# Sidebar filters
# ----------------------------
st.sidebar.header("Filters")
districts = df['district'].unique().tolist()
selected_districts = st.sidebar.multiselect("Select District(s):", districts, default=districts)

weeks = sorted(df['week'].unique())
selected_weeks = st.sidebar.multiselect("Select Week(s):", weeks, default=weeks)

filtered_df = df[(df['district'].isin(selected_districts)) & (df['week'].isin(selected_weeks))]

# ----------------------------
# Top metrics
# ----------------------------
st.title("Community Fever & Malaria Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Reports", len(filtered_df))
col2.metric("Fever Cases", (filtered_df['fever_last_48h']=='yes').sum())
malaria_tested = filtered_df[filtered_df['malaria_test_result']!='not_tested']
col3.metric("Malaria Tests", len(malaria_tested))
col4.metric("Malaria Positives", (malaria_tested['malaria_test_result']=='positive').sum())

# ----------------------------
# Weekly Fever Trend
# ----------------------------
weekly_trend = filtered_df.groupby(['district','week'])['fever_last_48h'].apply(lambda x: (x=='yes').sum()).reset_index(name='fever_cases')
st.subheader("Weekly Fever Cases by District")
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=weekly_trend, x='week', y='fever_cases', hue='district', marker='o', ax=ax)
ax.set_xlabel("Week Number")
ax.set_ylabel("Fever Cases")
ax.set_title("Weekly Fever Cases")
st.pyplot(fig)

# ----------------------------
# Malaria Positivity Rate
# ----------------------------
malaria_rate = malaria_tested.groupby('district')['malaria_test_result'].apply(lambda x: (x=='positive').sum()/len(x)*100).reset_index(name='malaria_positive_rate')
st.subheader("Malaria Positivity Rate by District (%)")
fig2, ax2 = plt.subplots(figsize=(7,5))
sns.barplot(data=malaria_rate, x='district', y='malaria_positive_rate', palette='Reds', ax=ax2)
ax2.set_ylabel("Positive Cases (%)")
ax2.set_xlabel("District")
st.pyplot(fig2)

# ----------------------------
# Mosquito Net Effect Table
# ----------------------------
net_effect = filtered_df.groupby('mosquito_net_use')['malaria_test_result'].apply(lambda x: (x=='positive').sum()/len(x)*100).reset_index(name='malaria_positive_rate')
st.subheader("Malaria Positivity vs Mosquito Net Use")
st.dataframe(net_effect)

# ----------------------------
# Interactive Map with Tooltips
# ----------------------------
st.subheader("Fever Cases Map")
uganda_map = folium.Map(location=[1.5, 32.5], zoom_start=6)

# Individual markers
for idx, row in filtered_df.iterrows():
    lat, lon = map(float, row['gps_location'].split(','))
    if row['fever_last_48h']=='yes':
        color = 'red'
        radius = 5
    else:
        color = 'blue'
        radius = 3
    tooltip = f"District: {row['district']}<br>Village: {row['village']}<br>Fever: {row['fever_last_48h']}<br>Malaria: {row['malaria_test_result']}"
    folium.CircleMarker(location=[lat, lon], radius=radius, color=color,
                        fill=True, fill_opacity=0.7, tooltip=tooltip).add_to(uganda_map)

# ----------------------------
# Fever Heatmap Layer
# ----------------------------
fever_points = filtered_df[filtered_df['fever_last_48h']=='yes'][['gps_location']].copy()
heat_data = [[float(latlon.split(',')[0]), float(latlon.split(',')[1])] for latlon in fever_points['gps_location']]
HeatMap(heat_data, radius=15, blur=10).add_to(uganda_map)

st_folium(uganda_map, width=800, height=500)

# ----------------------------
# Download buttons
# ----------------------------
st.subheader("Download Data & Plots")

# CSV download
csv_buffer = BytesIO()
filtered_df.to_csv(csv_buffer, index=False)
st.download_button(
    label="Download Filtered Dataset (CSV)",
    data=csv_buffer.getvalue(),
    file_name="filtered_surveillance_data.csv",
    mime="text/csv"
)

# PNG download for weekly fever trend
png_buffer = BytesIO()
fig.savefig(png_buffer, format='png', dpi=300)
st.download_button(
    label="Download Weekly Fever Trend Plot (PNG)",
    data=png_buffer.getvalue(),
    file_name="weekly_fever_trend.png",
    mime="image/png"
)

# PNG download for malaria positivity
png_buffer2 = BytesIO()
fig2.savefig(png_buffer2, format='png', dpi=300)
st.download_button(
    label="Download Malaria Positivity Plot (PNG)",
    data=png_buffer2.getvalue(),
    file_name="malaria_positivity_rate.png",
    mime="image/png"
)