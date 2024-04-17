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
all_years = st.sidebar.checkbox("Show data for all years", value=True)
if all_years:
    years = (2004, 2024)

compare_parties = st.sidebar.checkbox("Compare Political Parties", True)
if compare_parties:
    parties = st.sidebar.multiselect("Select parties to compare", ["BJP", "INC"], default=["BJP", "INC"])
else:
    party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])

# Filtering data
def filter_data(df, years):
    return df[df['Year'].between(years[0], years[1])]

# Display selected domain breakdown
selected_domain = st.selectbox("Select a domain to see the breakdown of issues", domain_mapping['Domains'].unique())
st.subheader(f"Breakdown of '{selected_domain}' domain")

for df, label in [(bjp_df, "BJP"), (inc_df, "INC")]:
    if compare_parties and label in parties or not compare_parties and party == label:
        domain_data = filter_data(df, years)
        domain_data = domain_data[domain_data['Domains'].str.contains(selected_domain)]
        subcategories = domain_mapping[domain_mapping['Domains'].str.contains(selected_domain)]['Subcategories'].tolist()[0].split(',')
        domain_count = pd.Series([x.strip() for subcat in domain_data['Topic_Subcategories'].tolist() for x in subcat.split(',') if x.strip() in subcategories]).value_counts()
        st.bar_chart(domain_count, use_container_width=True)

# Issue trend analysis
issue_selection = st.multiselect("Select issues to track", domain_mapping['Subcategories'].unique())
if issue_selection:
    fig = px.line(filter_data(bjp_df if not compare_parties or party == "BJP" else inc_df, years),
                  x='Year', y=[sub for sub in issue_selection if sub in domain_mapping['Subcategories'].unique()],
                  title='Trend of Selected Issues Over Years')
    st.plotly_chart(fig, use_container_width=True)
    if compare_parties:
        fig = px.line(filter_data(inc_df, years),
                      x='Year', y=[sub for sub in issue_selection if sub in domain_mapping['Subcategories'].unique()],
                      title='Trend of Selected Issues Over Years')
        st.plotly_chart(fig, use_container_width=True)
