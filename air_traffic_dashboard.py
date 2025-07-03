import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide")
st.title("✈️ Air Traffic Landing Analysis Dashboard")

# Load the dataset
df = pd.read_csv("Cleaned_Airtrafficdataset.csv")

# Fill missing values
df.fillna({
    'Operating Airline IATA Code': 'Unknown IATA',
    'Published Airline IATA Code': 'Unknown IATA',
    'Aircraft Model': 'Unknown Model',
    'Aircraft Version': 'Unknown Version',
    'Aircraft Manufacturer': 'Unknown Manufacturer',
    'Landing Aircraft Type': 'Unknown Type',
    'Aircraft Body Type': 'Unknown Body'
}, inplace=True)

# Convert Activity Period to datetime
df['Activity Period'] = pd.to_datetime(df['Activity Period'], format='%Y%m')

# Sidebar filter
airlines = df['Operating Airline'].unique()
selected_airlines = st.sidebar.multiselect("Filter by Operating Airline", airlines, default=airlines[:5])
filtered_df = df[df['Operating Airline'].isin(selected_airlines)]

# 1. Total Landed Weight by Airline and IATA Code
st.subheader("1. Total Landed Weight by Airline and IATA Code")
weight_df = filtered_df.groupby(['Operating Airline', 'Operating Airline IATA Code'])['Total Landed Weight'].sum().reset_index().sort_values(by='Total Landed Weight', ascending=False)
fig1 = px.bar(weight_df, x='Operating Airline', y='Total Landed Weight', color='Operating Airline IATA Code', title='Total Landed Weight by Airline and IATA Code')
st.plotly_chart(fig1, use_container_width=True)

# 2. Geographic Summary & Region vs Landing Count
st.subheader("2. Geographic Summaries & Regions vs Landing Counts")
geo_df = filtered_df.groupby(['GEO Summary', 'GEO Region'])['Landing Count'].sum().reset_index()
fig2 = px.sunburst(geo_df, path=['GEO Region', 'GEO Summary'], values='Landing Count', title='Landing Counts by Region and Summary')
st.plotly_chart(fig2, use_container_width=True)

# 3. Aircraft Manufacturers and Models by Airline
st.subheader("3. Most Common Aircraft Manufacturers & Models by Airline")
manufacturer_df = filtered_df.groupby(['Aircraft Manufacturer', 'Aircraft Model', 'Operating Airline'])['Landing Count'].sum().reset_index().sort_values(by='Landing Count', ascending=False).head(20)
fig3 = px.bar(manufacturer_df, x='Landing Count', y='Aircraft Manufacturer', color='Operating Airline', orientation='h', title='Top Aircraft Manufacturers by Airline')
st.plotly_chart(fig3, use_container_width=True)

# 4. Landing Trends Over Time by Airline and Aircraft Type
st.subheader("4. Landing Trends Over Time")

trend_airline = filtered_df.groupby(['Activity Period', 'Operating Airline'])['Landing Count'].sum().reset_index()
fig4 = px.line(trend_airline, x='Activity Period', y='Landing Count', color='Operating Airline', title='Landing Trends Over Time by Airline')
st.plotly_chart(fig4, use_container_width=True)

trend_type = filtered_df.groupby(['Activity Period', 'Landing Aircraft Type'])['Landing Count'].sum().reset_index()
fig5 = px.line(trend_type, x='Activity Period', y='Landing Count', color='Landing Aircraft Type', title='Landing Trends Over Time by Aircraft Type')
st.plotly_chart(fig5, use_container_width=True)

# 5. Aircraft Body Type Distribution by Region and Airline
st.subheader("5. Aircraft Body Type Distribution")

body_region = filtered_df.groupby(['GEO Region', 'Aircraft Body Type']).size().reset_index(name='Count')
fig6 = px.sunburst(body_region, path=['GEO Region', 'Aircraft Body Type'], values='Count', title='Aircraft Body Types by Geographic Region')
st.plotly_chart(fig6, use_container_width=True)

body_airline = filtered_df.groupby(['Operating Airline', 'Aircraft Body Type']).size().reset_index(name='Count')
fig7 = px.bar(body_airline, x='Operating Airline', y='Count', color='Aircraft Body Type', barmode='stack', title='Aircraft Body Types Across Airlines')
st.plotly_chart(fig7, use_container_width=True)

# 6. Correlation Between Landing Count and Total Landed Weight
st.subheader("6. Correlation Between Landing Count and Total Landed Weight")

corr_df = filtered_df.groupby(['Operating Airline', 'Landing Aircraft Type'])[['Landing Count', 'Total Landed Weight']].sum().reset_index()
fig8, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=corr_df, x='Landing Count', y='Total Landed Weight', hue='Operating Airline', style='Landing Aircraft Type', s=100, ax=ax)
ax.set_title("Landing Count vs Total Landed Weight")
st.pyplot(fig8)

# Show correlation matrix
correlation = corr_df[['Landing Count', 'Total Landed Weight']].corr()
st.write("Correlation Matrix:")
st.dataframe(correlation)
