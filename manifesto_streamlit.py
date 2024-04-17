import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the dataframes
url_bjp = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_BJP.csv'
url_inc = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_INC.csv'
url_domain_mapping = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/India_Manifesto_Topic_Classification.csv'

bjp_df = pd.read_csv(url_bjp)
inc_df = pd.read_csv(url_inc)
domain_mapping = pd.read_csv(url_domain_mapping)

# Create a mapping between subcategories and domains
subcategory_domain_mapping = dict(zip(domain_mapping['Subcategories'], domain_mapping['Domains']))

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

# Add an option to select a subcategory
subcategories = ['Agriculture', 'Caste', 'Culture and Morality', 'Democracy', 'Economic Planning and Goals', 'Employment',
                 'Environment and Sustainability', 'Federalism', 'Food and Public Distribution System', 'Freedom and Human Rights',
                 'Freemarket economy', 'Governmental and Administrative Efficiency', 'Health and Education', 'Inequality', 'Inflation',
                 'Influence of foreign countries', 'Internal Security', 'Jammu and Kashmir', 'Judiciary', 'Labour Rights', 'Law and Order',
                 'Leader\'s superior competence', 'National security goals', 'Nationalism and Patriotism', 'Party\'s superior competence',
                 'Physical Infrastructure and Transportation', 'Political Corruption', 'Pro-state intervention', 'Religion', 'Rural Development',
                 'Science and Technology', 'Terrorism', 'Underprivileged Minorities', 'Urban Development', 'Welfare State Expansion', 'Women',
                 'World Peace and Internationalism']
selected_subcategory = st.sidebar.selectbox("Select a subcategory", subcategories)

if compare_parties:
   # Display the most common domains as radar charts
   st.subheader("Most Common Domains for {} and {} from [{}] to [{}]".format(parties[0], parties[1], years[0], years[1]))

   bjp_subcategory_counts = {}
   inc_subcategory_counts = {}

   for subcategory in subcategories:
       bjp_subcategory_counts[subcategory] = bjp_df[bjp_df['Year'].between(years[0], years[1])][subcategory].sum()
       inc_subcategory_counts[subcategory] = inc_df[inc_df['Year'].between(years[0], years[1])][subcategory].sum()

   bjp_domain_counts = {subcategory_domain_mapping[subcategory]: count for subcategory, count in bjp_subcategory_counts.items() if subcategory in subcategory_domain_mapping}
   inc_domain_counts = {subcategory_domain_mapping[subcategory]: count for subcategory, count in inc_subcategory_counts.items() if subcategory in subcategory_domain_mapping}

   col1, col2 = st.columns(2)
   with col1:
       fig = go.Figure(go.Scatterpolar(
           r=list(bjp_domain_counts.values()),
           theta=list(bjp_domain_counts.keys()),
           fill='toself',
           name='BJP'
       ))
       fig.update_layout(
           polar=dict(
               radialaxis=dict(
                   visible=True,
                   range=[0, max(list(bjp_domain_counts.values()))],
                   tickfont=dict(size=10)
               )),
           showlegend=True,
           margin=dict(t=20, b=20, l=20, r=20),
           height=500
       )
       st.plotly_chart(fig, use_container_width=True)

   with col2:
       fig = go.Figure(go.Scatterpolar(
           r=list(inc_domain_counts.values()),
           theta=list(inc_domain_counts.keys()),
           fill='toself',
           name='INC'
       ))
       fig.update_layout(
           polar=dict(
               radialaxis=dict(
                   visible=True,
                   range=[0, max(list(inc_domain_counts.values()))],
                   tickfont=dict(size=10)
               )),
           showlegend=True,
           margin=dict(t=20, b=20, l=20, r=20),
           height=500
       )
       st.plotly_chart(fig, use_container_width=True)

   # Display the most common issues
   st.subheader("Most Common Issues for {} and {} from [{}] to [{}]".format(parties[0], parties[1], years[0], years[1]))

   bjp_subcategory_counts = {subcategory: bjp_df[bjp_df['Year'].between(years[0], years[1])][subcategory].sum() for subcategory in subcategories}
   bjp_subcategory_counts = dict(sorted(bjp_subcategory_counts.items(), key=lambda item: item[1], reverse=True))

   inc_subcategory_counts = {subcategory: inc_df[inc_df['Year'].between(years[0], years[1])][subcategory].sum() for subcategory in subcategories}
   inc_subcategory_counts = dict(sorted(inc_subcategory_counts.items(), key=lambda item: item[1], reverse=True))

   col1, col2 = st.columns(2)
   with col1:
       st.subheader("{} Most Common Issues".format(parties[0]))
       st.bar_chart(pd.Series(bjp_subcategory_counts))
   with col2:
       st.subheader("{} Most Common Issues".format(parties[1]))
       st.bar_chart(pd.Series(inc_subcategory_counts))

   # Display the line chart for the selected subcategory
   st.subheader("Trend for '{}' from [{}] to [{}]".format(selected_subcategory, years[0], years[1]))

   bjp_subcategory_data = bjp_df.groupby('Year')[selected_subcategory].sum().reset_index()
   inc_subcategory_data = inc_df.groupby('Year')[selected_subcategory].sum().reset_index()

   fig = go.Figure()
   fig.add_trace(go.Scatter(x=bjp_subcategory_data['Year'], y=bjp_subcategory_data[selected_subcategory], mode='lines', name='BJP'))
   fig.add_trace(go.Scatter(x=inc_subcategory_data['Year'], y=inc_subcategory_data[selected_subcategory], mode='lines', name='INC'))

   fig.update_layout(
       xaxis_title='Year',
       yaxis_title='Count',
       legend=dict(
           orientation="h",
           yanchor="bottom",
           y=1.02,
           xanchor="right",
           x=1
       ),
       margin=dict(t=20, b=20, l=20, r=20),
       height=500
