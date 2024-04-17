import streamlit as st
import pandas as pd

# Load the dataframes
url_bjp = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_BJP.csv'
url_inc = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_INC.csv'

bjp_df = pd.read_csv(url_bjp)
inc_df = pd.read_csv(url_inc)

# Create the Streamlit app
st.title("Election Manifesto Dashboard")

# Sidebar for selecting the years and compare option
year_min = 2004
year_max = 2024
year_step = 5
years = st.sidebar.slider("Select years", min_value=year_min, max_value=year_max, value=(year_min, year_max), step=year_step)
all_years = st.sidebar.checkbox("Show data for all years")
if all_years:
    years = (year_min, year_max)

compare_parties = st.sidebar.checkbox("Compare Political Parties")
if compare_parties:
    parties = st.sidebar.multiselect("Select parties to compare", ["BJP", "INC"], default=["BJP", "INC"])
else:
    party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])

# Display data frames based on selected options
if compare_parties:
    st.subheader(f"Manifesto Comparisons for {parties} from {years[0]} to {years[1]}")
    if "BJP" in parties:
        st.subheader("BJP Manifesto")
        st.dataframe(bjp_df[bjp_df['Year'].between(years[0], years[1])])
    if "INC" in parties:
        st.subheader("INC Manifesto")
        st.dataframe(inc_df[inc_df['Year'].between(years[0], years[1])])
else:
    st.subheader(f"Manifesto for {party} from {years[0]} to {years[1]}")
    df = bjp_df if party == "BJP" else inc_df
    st.dataframe(df[df['Year'].between(years[0], years[1])])
