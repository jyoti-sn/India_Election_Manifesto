import streamlit as st
import pandas as pd

# Load the dataframes (assuming URLs are still valid)
url_bjp = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_BJP.csv'
url_inc = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_INC.csv'

bjp_df = pd.read_csv(url_bjp)
inc_df = pd.read_csv(url_inc)

# App title
st.title("Election Manifesto Dashboard")

# Sidebar for year and party selection
years = st.sidebar.slider(
    "Select years", min_value=2004, max_value=2024, value=(2004, 2024), step=5
)
party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])

# Filter data based on selected year range and party
df = bjp_df if party == "BJP" else inc_df
df = df[df['Year'].between(years[0], years[1])]

# Get subcategories and their counts
subcategories = [
    x.strip() for subcategory in df['Topic_Subcategories'].tolist() for x in subcategory.split(',')
]
subcategory_counts = pd.Series(subcategories).value_counts()

# Display most common issues
st.subheader(f"Most Common Issues for {party} from [{years[0]}] to [{years[1]}]")
st.bar_chart(subcategory_counts.nlargest(10))  # Show top 10
