import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
if compare_parties:
    parties = st.sidebar.multiselect("Select parties to compare", ["BJP", "INC"], default=["BJP", "INC"])
else:
    party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])

# Prepare subcategory data
issue_columns = ['Agriculture', 'Caste', 'Culture and Morality', 'Democracy', 'Economic Planning and Goals', 'Employment',
                 'Environment and Sustainability', 'Federalism', 'Food and Public Distribution System', 'Freedom and Human Rights',
                 'Freemarket economy', 'Governmental and Administrative Efficiency', 'Health and Education', 'Inequality', 'Inflation',
                 'Influence of foreign countries', 'Internal Security', 'Jammu and Kashmir', 'Judiciary', 'Labour Rights', 'Law and Order',
                 'Leader\'s superior competence', 'National security goals', 'Nationalism and Patriotism', 'Party\'s superior competence',
                 'Physical Infrastructure and Transportation', 'Political Corruption', 'Pro-state intervention', 'Religion', 'Rural Development',
                 'Science and Technology', 'Terrorism', 'Underprivileged Minorities', 'Urban Development', 'Welfare State Expansion', 'Women',
                 'World Peace and Internationalism']

# Subcategories to domains
subcategory_to_domain = domain_mapping.set_index('Subcategories')['Domains'].to_dict()

# Display Radar Charts for Domains
if compare_parties:
    st.subheader(f"Domain Comparison for {parties[0]} and {parties[1]} from {years[0]} to {years[1]}")
    domain_dfs = {}
    for party in parties:
        df = bjp_df if party == "BJP" else inc_df
        df = df[df['Year'].between(years[0], years[1])]
        df = df[issue_columns].sum().reset_index()
        df.columns = ['Subcategory', 'Count']
        df['Domain'] = df['Subcategory'].map(subcategory_to_domain)
        domain_df = df.groupby('Domain')['Count'].sum().reset_index()
        domain_dfs[party] = domain_df

        fig = px.line_polar(domain_dfs[party], r='Count', theta='Domain', line_close=True, title=f"{party} Domain Distribution")
        st.plotly_chart(fig, use_container_width=True)

# Select subcategories for line chart
selected_subcategories = st.sidebar.multiselect("Select subcategories for line chart", issue_columns)
if selected_subcategories:
    st.subheader("Subcategory Trends Over Years")
    for subcategory in selected_subcategories:
        if compare_parties:
            fig = go.Figure()
            for party in parties:
                df = bjp_df if party == "BJP" else inc_df
                sub_df = df.groupby('Year')[subcategory].sum().reset_index()
                fig.add_trace(go.Scatter(x=sub_df['Year'], y=sub_df[subcategory], mode='lines+markers', name=f"{party} - {subcategory}"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            df = bjp_df if party == "BJP" else inc_df
            sub_df = df.groupby('Year')[subcategory].sum().reset_index()
            fig = px.line(sub_df, x='Year', y=subcategory, title=f"{party} - {subcategory} Trends")
            st.plotly_chart(fig, use_container_width=True)

