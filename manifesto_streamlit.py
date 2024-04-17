import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

# Load dataframes (assuming URLs are still valid)
url_bjp = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_BJP.csv'
url_inc = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_INC.csv'

bjp_df = pd.read_csv(url_bjp)
inc_df = pd.read_csv(url_inc)

# Load party logos (make sure these paths are correct)
bjp_logo = Image.open("path/to/bjp_logo.png")  # Replace with your BJP logo path
inc_logo = Image.open("path/to/inc_logo.png")  # Replace with your INC logo path

# App title and description
st.title("Election Manifesto Dashboard")
st.subheader("Exploring the Evolution of Key Issues in Indian Election Manifestos")

# Sidebar for year and party selection
years = st.sidebar.slider(
    "Select years", min_value=2004, max_value=2024, value=(2004, 2024), step=5
)
compare_parties = st.sidebar.checkbox("Compare Political Parties")

if compare_parties:
    parties = st.sidebar.multiselect("Select parties to compare", ["BJP", "INC"], default=["BJP", "INC"])
else:
    party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])

# Function to generate radar chart with party-specific colors
def generate_radar_chart(party_name, df):
    domains = [x.strip() for domain in df['Domains'].tolist() for x in domain.split(',')]
    domain_counts = pd.Series(domains).value_counts()
    color = "orange" if party_name == "BJP" else "blue"  # Set color based on party
    fig = go.Figure(go.Scatterpolar(
        r=domain_counts.nlargest(10),
        theta=domain_counts.nlargest(10).index,
        fill='toself',
        name=party_name,
        line_color=color
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(domain_counts)],
                tickfont=dict(size=10)
            )
        ),
        showlegend=True,
        margin=dict(t=30, b=30, l=30, r=30)
    )
    return fig

# Function to generate bar chart with party-specific colors 
def generate_subcategory_barchart(party_name, df):
    subcategories = [x.strip() for subcategory in df['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
    subcategory_counts = pd.Series(subcategories).value_counts()
    color = "orange" if party_name == "BJP" else "blue"  # Set color based on party
    st.subheader(f"{party_name} Most Common Issues")
    st.bar_chart(subcategory_counts.nlargest(10), color=color) 

# Logic for comparing parties
if compare_parties:
    st.subheader("Most Common Domains")
    col1, col2 = st.columns(2)
    with col1:
        bjp_filtered = bjp_df[bjp_df['Year'].between(years[0], years[1])]
        st.image(bjp_logo, width=100)  # Display BJP logo
        st.plotly_chart(generate_radar_chart("BJP", bjp_filtered), use_container_width=True)
    with col2:
        inc_filtered = inc_df[inc_df['Year'].between(years[0], years[1])]
        st.image(inc_logo, width=100)  # Display INC logo
        st.plotly_chart(generate_radar_chart("INC", inc_filtered), use_container_width=True)

    st.subheader("Most Common Issues")
    col3, col4 = st.columns(2)
    with col3:
        generate_subcategory_barchart("BJP", bjp_filtered) 
    with col4:
        generate_subcategory_barchart("INC", inc_filtered) 

# Logic for single party selection
else:
    df = bjp_df if party == "BJP" else inc_df
    filtered_df = df[df['Year'].between(years[0], years[1])]
    
    if party == "BJP": 
        st.image(bjp_logo, width=100) 
    else:
        st.image(inc_logo, width=100) 
    
    st.subheader("Most Common Domains")
    st.plotly_chart(generate_radar_chart(party, filtered_df), use_container_width=True)

    st.subheader("Most Common Issues")
    generate_subcategory_barchart(party, filtered_df)
