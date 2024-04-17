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


if compare_parties:
    # Display the most common domains as radar charts
    st.subheader("Most Common Domains for {} and {} from [{}] to [{}]".format(parties[0], parties[1], years[0], years[1]))
    
    if "BJP" in parties:
        bjp_topics = [x.strip() for topic in bjp_df[bjp_df['Year'].between(years[0], years[1])]['Domains'].tolist() for x in topic.split(',')]
        bjp_topic_counts = pd.Series(bjp_topics).value_counts()
        bjp_topic_counts = bjp_topic_counts.reindex(bjp_topic_counts.nlargest(10).index)

    if "INC" in parties:
        inc_topics = [x.strip() for topic in inc_df[inc_df['Year'].between(years[0], years[1])]['Domains'].tolist() for x in topic.split(',')]
        inc_topic_counts = pd.Series(inc_topics).value_counts()
        inc_topic_counts = inc_topic_counts.reindex(inc_topic_counts.nlargest(10).index)

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(go.Scatterpolar(
            r=bjp_topic_counts,
            theta=bjp_topic_counts.index,
            fill='toself',
            name='BJP'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(bjp_topic_counts)],
                    tickfont=dict(size=10)
                )),
            showlegend=True,
            margin=dict(t=20, b=20, l=20, r=20),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure(go.Scatterpolar(
            r=inc_topic_counts,
            theta=inc_topic_counts.index,
            fill='toself',
            name='INC'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(inc_topic_counts)],
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
        bjp_subcategories = [x.strip() for subcategory in bjp_df[bjp_df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
        bjp_subcategory_counts = pd.Series(bjp_subcategories).value_counts()
        bjp_subcategory_counts = bjp_subcategory_counts.reindex(bjp_subcategory_counts.nlargest(10).index)

    if "INC" in parties:
        inc_subcategories = [x.strip() for subcategory in inc_df[inc_df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
        inc_subcategory_counts = pd.Series(inc_subcategories).value_counts()
        inc_subcategory_counts = inc_subcategory_counts.reindex(inc_subcategory_counts.nlargest(10).index)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("{} Most Common Issues".format(parties[0]))
        st.bar_chart(bjp_subcategory_counts.rename(index=str, columns={'value': 'Count'}))  # Rename the index and column names
    with col2:
        st.subheader("{} Most Common Issues".format(parties[1]))
        st.bar_chart(inc_subcategory_counts.rename(index=str, columns={'value': 'Count'}))  # Rename the index and column names
else:
    df = bjp_df if party == "BJP" else inc_df

    # Display the most common domains as a radar chart
    st.subheader("Most Common Domains for {} from [{}] to [{}]".format(party, years[0], years[1]))
    topics = [x.strip() for topic in df[df['Year'].between(years[0], years[1])]['Domains'].tolist() for x in topic.split(',')]
    topic_counts = pd.Series(topics).value_counts()
    topic_counts = topic_counts.reindex(topic_counts.nlargest(10).index)

    fig = go.Figure(go.Scatterpolar(
        r=topic_counts,
        theta=topic_counts.index,
        fill='toself'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(topic_counts)],
            tickfont=dict(size=10)
        )),
    showlegend=False,
    margin=dict(t=20, b=20, l=20, r=20),
    height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Display the most common issues
    st.subheader("Most Common Issues for {} from [{}] to [{}]".format(party, years[0], years[1]))
    subcategories = [x.strip() for subcategory in df[df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
    subcategory_counts = pd.Series(subcategories).value_counts()
    subcategory_counts = subcategory_counts.reindex(subcategory_counts.nlargest(10).index)
    st.bar_chart(subcategory_counts.rename(index=str, columns={'value': 'Count'}))  # Rename the index and column names
