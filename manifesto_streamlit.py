import streamlit as st
import pandas as pd
import plotly.express as px

# Assuming the modified dataframes are loaded directly or this script is placed after data preprocessing
url_bjp = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_BJP.csv'
url_inc = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_INC.csv'

bjp_df = pd.read_csv(url_bjp)
inc_df = pd.read_csv(url_inc)

# Create the Streamlit app
st.title("India Election Manifesto Dashboard")

# Sidebar for selecting the years
years = st.sidebar.slider("Select years", 2004, 2024, (2004, 2024), 5)
all_years = st.sidebar.checkbox("Show data for all years")
if all_years:
    years = (2004, 2024)

compare_parties = st.sidebar.checkbox("Compare Political Parties", True)

# Sidebar to select subcategories for trend analysis
subcategories_list = bjp_df.columns[bjp_df.columns.str.contains('_')].str.replace('_', ' ').tolist()  # Assuming preprocessing replaced spaces with underscores
selected_subcategories = st.sidebar.multiselect("Select subcategories to track", subcategories_list)

# Function to plot data
def plot_subcategory_trends(df, subcategory, years, party_name):
    # Filter the dataframe by years
    filtered_df = df[df['Year'].between(years[0], years[1])]
    
    # Creating the line chart for the selected subcategory
    if subcategory in filtered_df.columns:
        fig = px.line(
            filtered_df,
            x='Year',
            y=subcategory,
            labels={'Year': 'Year', subcategory: 'Count'},
            title=f"{subcategory.title().replace('_', ' ')} Trend for {party_name}"
        )
        st.plotly_chart(fig, use_container_width=True)

# Displaying charts based on selected subcategories
for subcategory in selected_subcategories:
    subcategory_col = subcategory.replace(' ', '_')  # If preprocessing replaced spaces with underscores
    if compare_parties:
        plot_subcategory_trends(bjp_df, subcategory_col, years, "BJP")
        plot_subcategory_trends(inc_df, subcategory_col, years, "INC")
    else:
        df = bjp_df if st.sidebar.radio("Select Party", ("BJP", "INC")) == "BJP" else inc_df
        plot_subcategory_trends(df, subcategory_col, years, df.iloc[0]['Party'])

# Other components of the dashboard (if any)
# e.g., Comparisons, summaries, etc.

