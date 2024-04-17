import streamlit as st
import pandas as pd
import plotly.graph_objects as go

url_bjp = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_BJP.csv'
url_inc = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_INC.csv'
url_domain_mapping = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/India_Manifesto_Topic_Classification.csv'

bjp_df = pd.read_csv(url_bjp)
inc_df = pd.read_csv(url_inc)
mapping_df = pd.read_csv(url_domain_mapping)

# Sidebar filters
st.sidebar.title("Filters")

# Sidebar for selecting the years and compare option
years = st.sidebar.slider("Select years", 2004, 2024, (2004, 2024), 5)
all_years = st.sidebar.checkbox("Show data for all years")
if all_years:
    years = (2004, 2024)

# Apply year filter
filtered_bjp_df = bjp_df[bjp_df['Year'].isin(range(years[0], years[1] + 1))]
filtered_inc_df = inc_df[inc_df['Year'].isin(range(years[0], years[1] + 1))]

# Party selection
party_selection = st.sidebar.radio("Select Party", ["Compare BJP and INC", "BJP", "INC"])

# Apply filters
if party_selection == "Compare BJP and INC":
    filtered_bjp_df = bjp_df[bjp_df['Year'].isin(selected_year)]
    filtered_inc_df = inc_df[inc_df['Year'].isin(selected_year)]
else:
    if party_selection == "BJP":
        filtered_df = bjp_df[bjp_df['Year'].isin(selected_year)]
    else:
        filtered_df = inc_df[inc_df['Year'].isin(selected_year)]

# Top 10 subcategories
st.header("Top 10 Subcategories")
if party_selection == "Compare BJP and INC":
    top_bjp_subcategories = filtered_bjp_df[subcategory_columns].sum().sort_values(ascending=False)[:10]
    top_inc_subcategories = filtered_inc_df[subcategory_columns].sum().sort_values(ascending=False)[:10]
    st.write("BJP:")
    st.bar_chart(top_bjp_subcategories)
    st.write("INC:")
    st.bar_chart(top_inc_subcategories)
else:
    top_subcategories = filtered_df[subcategory_columns].sum().sort_values(ascending=False)[:10]
    st.bar_chart(top_subcategories)

# Radar chart for domains
st.header("Radar Chart for Domains")
if party_selection == "Compare BJP and INC":
    bjp_domain_counts = filtered_bjp_df.merge(mapping_df, left_on='Topic_Subcategories', right_on='Subcategories', how='left')
    inc_domain_counts = filtered_inc_df.merge(mapping_df, left_on='Topic_Subcategories', right_on='Subcategories', how='left')
    bjp_domain_counts = bjp_domain_counts.groupby('Domains')[subcategory_columns].sum().reset_index()
    inc_domain_counts = inc_domain_counts.groupby('Domains')[subcategory_columns].sum().reset_index()
    st.write("BJP:")
    st.plotly_chart(create_radar_chart(bjp_domain_counts))
    st.write("INC:")
    st.plotly_chart(create_radar_chart(inc_domain_counts))
else:
    domain_counts = filtered_df.merge(mapping_df, left_on='Topic_Subcategories', right_on='Subcategories', how='left')
    domain_counts = domain_counts.groupby('Domains')[subcategory_columns].sum().reset_index()
    st.plotly_chart(create_radar_chart(domain_counts))

# Subcategories for selected domain
st.header("Subcategories for Selected Domain")
selected_domain = st.selectbox("Select Domain", mapping_df['Domains'].unique())
if party_selection == "Compare BJP and INC":
    bjp_subcategory_counts = filtered_bjp_df.merge(mapping_df[mapping_df['Domains'] == selected_domain], left_on='Topic_Subcategories', right_on='Subcategories', how='left')[subcategory_columns].sum().reset_index()
    inc_subcategory_counts = filtered_inc_df.merge(mapping_df[mapping_df['Domains'] == selected_domain], left_on='Topic_Subcategories', right_on='Subcategories', how='left')[subcategory_columns].sum().reset_index()
    st.write("BJP:")
    st.bar_chart(bjp_subcategory_counts.set_index('Subcategories'))
    st.write("INC:")
    st.bar_chart(inc_subcategory_counts.set_index('Subcategories'))
else:
    subcategory_counts = filtered_df.merge(mapping_df[mapping_df['Domains'] == selected_domain], left_on='Topic_Subcategories', right_on='Subcategories', how='left')[subcategory_columns].sum().reset_index()
    st.bar_chart(subcategory_counts.set_index('Subcategories'))

# Line chart for selected subcategory
st.header("Line Chart for Selected Subcategory")
selected_subcategory = st.selectbox("Select Subcategory", mapping_df['Subcategories'].unique())
if party_selection == "Compare BJP and INC":
    bjp_subcategory_trend = bjp_df.groupby('Year')[selected_subcategory].sum().reset_index()
    inc_subcategory_trend = inc_df.groupby('Year')[selected_subcategory].sum().reset_index()
    st.line_chart(bjp_subcategory_trend.set_index('Year'), color='blue', label='BJP')
    st.line_chart(inc_subcategory_trend.set_index('Year'), color='red', label='INC')
else:
    subcategory_trend = filtered_df.groupby('Year')[selected_subcategory].sum().reset_index()
    st.line_chart(subcategory_trend.set_index('Year'))

# Helper function to create radar chart
def create_radar_chart(data):
    domains = data['Domains'].unique()
    fig = go.Figure()
    for domain in domains:
        fig.add_trace(go.Scatterpolar(
            r=data[data['Domains'] == domain][subcategory_columns].values[0],
            theta=subcategory_columns,
            fill='toself',
            name=domain
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(data[subcategory_columns].values.max()) + 10]
            )
        ),
        showlegend=True
    )
    return fig
