import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataframes
url_bjp = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_BJP.csv'
url_inc = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_INC.csv'
url_domain_mapping = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/India_Manifesto_Topic_Classification.csv'

bjp_df = pd.read_csv(url_bjp)
inc_df = pd.read_csv(url_inc)
domain_mapping = pd.read_csv(url_domain_mapping)

# Create the Streamlit app
st.title("India Election Manifesto Dashboard")

# Sidebar for selecting the years and compare option
years = st.sidebar.slider("Select years", 2004, 2024, (2004, 2024), 5)
all_years = st.sidebar.checkbox("Show data for all years")
if all_years:
    years = (2004, 2024)

compare_parties = st.sidebar.checkbox("Compare Political Parties")

# Sidebar to select an issue for trend analysis
selected_issue = st.sidebar.selectbox("Select an issue for trend analysis", domain_mapping['Subcategories'].unique())

# Filter data based on selected years
def filter_data_by_years(df, years):
    return df[df['Year'].between(years[0], years[1])]

# Prepare data for line chart visualization
def prepare_line_chart_data(df, issue, years):
    filtered_df = filter_data_by_years(df, years)
    issue_df = filtered_df[filtered_df['Topic_Subcategories'].str.contains(issue)]
    return issue_df.groupby('Year').count()['Manifesto']  # Assuming 'Manifesto' column exists; adjust as necessary

# Fetching data for line charts
bjp_issue_data = prepare_line_chart_data(bjp_df, selected_issue, years)
inc_issue_data = prepare_line_chart_data(inc_df, selected_issue, years)

# Plotting line charts
fig = px.line(
    x=bjp_issue_data.index, 
    y=bjp_issue_data.values, 
    labels={'x': 'Year', 'y': 'Count'},
    title=f"Year over Year Trend for {selected_issue} - BJP"
)
st.plotly_chart(fig, use_container_width=True)

fig = px.line(
    x=inc_issue_data.index, 
    y=inc_issue_data.values, 
    labels={'x': 'Year', 'y': 'Count'},
    title=f"Year over Year Trend for {selected_issue} - INC"
)
st.plotly_chart(fig, use_container_width=True)

