import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CO2 emissions dataset by country
co2_country_df = pd.read_csv('co2_emissions_kt_by_country.csv')

# Preprocess data: Rename columns to match expected column names
co2_country_df.rename(columns={'country_name': 'Country', 'year': 'Year', 'value': 'CO2_Emissions'}, inplace=True)

# Ensure 'Year' is numeric
co2_country_df['Year'] = pd.to_numeric(co2_country_df['Year'], errors='coerce')

# Sidebar filters
st.sidebar.header("Filter Options")
years = st.sidebar.slider("Select Year Range:", int(co2_country_df['Year'].min()), int(co2_country_df['Year'].max()), 
                          (int(co2_country_df['Year'].min()), int(co2_country_df['Year'].max())))
countries = st.sidebar.multiselect("Select Country(ies):", options=co2_country_df['Country'].unique(), 
                                   default=co2_country_df['Country'].unique())

# Filter data based on user selections
filtered_data = co2_country_df[(co2_country_df['Year'] >= years[0]) & 
                               (co2_country_df['Year'] <= years[1]) & 
                               (co2_country_df['Country'].isin(countries))]

# Dashboard title
st.title("CO2 Emissions Analysis by Country")

# Display total emissions
st.header("Overall CO2 Emissions")
total_emissions = filtered_data['CO2_Emissions'].sum()
st.metric(label="Total CO2 Emissions (tons)", value=f"{total_emissions:,.0f}")

# CO2 Emissions over time
st.subheader("CO2 Emissions Over Time")
emissions_over_time = filtered_data.groupby('Year')['CO2_Emissions'].sum().reset_index()

fig, ax = plt.subplots()
sns.lineplot(data=emissions_over_time, x='Year', y='CO2_Emissions', marker='o', ax=ax)
plt.title('CO2 Emissions Over Time')
plt.xlabel('Year')
plt.ylabel('CO2 Emissions (tons)')
plt.tight_layout()
st.pyplot(fig)

# CO2 Emissions by country
st.subheader("CO2 Emissions by Country")
emissions_by_country = filtered_data.groupby('Country')['CO2_Emissions'].sum().reset_index().sort_values(by='CO2_Emissions', ascending=False).head(10)

fig2, ax2 = plt.subplots()
sns.barplot(data=emissions_by_country, x='Country', y='CO2_Emissions', palette='viridis', ax=ax2)
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Countries by CO2 Emissions')
plt.tight_layout()
st.pyplot(fig2)

# Download filtered data
st.sidebar.header("Download Data")
st.sidebar.download_button(label="Download Filtered Data", data=filtered_data.to_csv(index=False), file_name='filtered_data.csv', mime='text/csv')

st.write("**Note:** Use the sidebar filters to explore data by year and country.")
