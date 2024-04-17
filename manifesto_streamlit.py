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

# Function to count occurrences of subcategories
def count_subcategories(df, years):
    subcategory_counts = df[df['Year'].between(years[0], years[1])][subcategories].sum(axis=0)
    return subcategory_counts

# Function to map subcategories to domains and count domain occurrences
def count_domains(subcategory_counts):
    domain_counts = subcategory_counts.rename(index=domain_mapping.set_index('Subcategories')['Domains']).groupby(level=0).sum()
    return domain_counts

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

# Subcategory selection for line chart
selected_subcategory = st.sidebar.selectbox("Select a subcategory for trend", subcategories)

# Define subcategories (issues)
subcategories = ['Agriculture', 'Caste', 'Culture and Morality',
       'Democracy', 'Economic Planning and Goals', 'Employment',
       'Environment and Sustainability', 'Federalism',
       'Food and Public Distribution System', 'Freedom and Human Rights',
       'Freemarket economy', 'Governmental and Administrative Efficiency',
       'Health and Education', 'Inequality', 'Inflation',
       'Influnce of foreign countries', 'Internal Security',
       'Jammu and Kashmir', 'Judiciary', 'Labour Rights', 'Law and Order',
       'Leader's superior competence', 'National security goals',
       'Nationalism and Patriotism', 'Party's superior competence',
       'Physical Infrastructure and Transportation', 'Political Corruption',
       'Pro-state intervention', 'Religion', 'Rural Development',
       'Science and Technology', 'Terrorism', 'Underprivileged Minorities',
       'Urban Development', 'Welfare State Expansion', 'Women',
       'World Peace and Internationalism']

if compare_parties:
    # Display the most common domains as radar charts
    st.subheader("Most Common Domains for {} and {} from [{}] to [{}]".format(parties[0], parties[1], years[0], years[1]))
    
    if "BJP" in parties:
        bjp_subcategory_counts = count_subcategories(bjp_df, years)
        bjp_domain_counts = count_domains(bjp_subcategory_counts).nlargest(10)

    if "INC" in parties:
        inc_subcategory_counts = count_subcategories(inc_df, years)
        inc_domain_counts = count_domains(inc_subcategory_counts).nlargest(10)

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(go.Scatterpolar(
            r=bjp_domain_counts,
            theta=bjp_domain_counts.index,
            fill='toself',
            name='BJP'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(bjp_domain_counts)],
                    tickfont=dict(size=10)
                )),
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure(go.Scatterpolar(
            r=inc_domain_counts,
            theta=inc_domain_counts.index,
            fill='toself',
            name='INC'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(inc_domain_counts)],
                    tickfont=dict(size=10)
                )),
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    # Display the most common issues
    st.subheader("Most Common Issues for {} and {} from [{}] to [{}]".format(parties[0], parties[1], years[0], years[1]))
    
    if "BJP" in parties:
        bjp_subcategory_counts = count_subcategories(bjp_df, years).nlargest(10)

    if "INC" in parties:
        inc_subcategory_counts = count_subcategories(inc_df, years).nlargest(10)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("{} Most Common Issues".format(parties[0]))
        st.bar_chart(bjp_subcategory_counts)
    with col2:
        st.subheader("{} Most Common Issues".format(parties[1]))
        st.bar_chart(inc_subcategory_counts)

    # Display subcategory trends
    st.subheader("Trend for {} over the Years".format(selected_subcategory))
    
    bjp_trend = bjp_df.groupby('Year')[selected_subcategory].sum()
    inc_trend = inc_df.groupby('Year')[selected_subcategory].sum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=bjp_trend.index, y=bjp_trend.values, name='BJP'))
    fig.add_trace(go.Scatter(x=inc_trend.index, y=inc_trend.values, name='INC'))
    fig.update_layout(xaxis_title='Year', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)

else:
    df = bjp_df if party == "BJP" else inc_df

    # Display the most common domains as a radar chart
    st.subheader("Most Common Domains for {} from [{}] to [{}]".format(party, years[0], years[1]))
    subcategory_counts = count_subcategories(df, years)
    domain_counts = count_domains(subcategory_counts).nlargest(10)

    fig = go.Figure(go.Scatterpolar(
        r=domain_counts,
        theta=domain_counts.index,
        fill='toself'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(domain_counts)],
            tickfont=dict(size=10)  # Added equals sign here
        )),
    showlegend=False,
    margin=dict(t=20, b=20, l=20, r=20),
    height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Display the most common issues
    st.subheader("Most Common Issues for {} from [{}] to [{}]".format(party, years[0], years[1]))
    subcategory_counts = count_subcategories(df, years).nlargest(10)
    st.bar_chart(subcategory_counts)

    # Display subcategory trend
    st.subheader("Trend for {} over the Years".format(selected_subcategory))
    trend = df.groupby('Year')[selected_subcategory].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trend.index, y=trend.values, name=party))
    fig.update_layout(xaxis_title='Year', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)
