import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

compare_parties = st.sidebar.checkbox("Compare BJP and INC")

# Define stop words and custom stop words
stop_words = ['the', 'and', 'a', 'in', 'to', 'of', 'for']
custom_stop_words = ['Bharatiya', 'Janata', 'Party']

if compare_parties:
    # Display the most common topics as a radar chart
    st.subheader("Most Common Topics")
    bjp_topics = [x.strip() for topic in bjp_df[bjp_df['Year'].between(years[0], years[1])]['Domains'].tolist() for x in topic.split(',')]
    bjp_topic_counts = pd.Series(bjp_topics).value_counts()
    bjp_topic_counts = bjp_topic_counts.reindex(bjp_topic_counts.nlargest(10).index)

    inc_topics = [x.strip() for topic in inc_df[inc_df['Year'].between(years[0], years[1])]['Domains'].tolist() for x in topic.split(',')]
    inc_topic_counts = pd.Series(inc_topics).value_counts()
    inc_topic_counts = inc_topic_counts.reindex(inc_topic_counts.nlargest(10).index)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=bjp_topic_counts,
        theta=bjp_topic_counts.index,
        fill='toself',
        name='BJP'
    ))
    fig.add_trace(go.Scatterpolar(
        r=inc_topic_counts,
        theta=inc_topic_counts.index,
        fill='toself',
        name='INC'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(bjp_topic_counts.max(), inc_topic_counts.max())]
            )),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display the most common subcategories
    st.subheader("Most Common Subcategories")
    bjp_subcategories = [x.strip() for subcategory in bjp_df[bjp_df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
    bjp_subcategory_counts = pd.Series(bjp_subcategories).value_counts()
    bjp_subcategory_counts = bjp_subcategory_counts.reindex(bjp_subcategory_counts.nlargest(10).index)

    inc_subcategories = [x.strip() for subcategory in inc_df[inc_df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
    inc_subcategory_counts = pd.Series(inc_subcategories).value_counts()
    inc_subcategory_counts = inc_subcategory_counts.reindex(inc_subcategory_counts.nlargest(10).index)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("BJP Most Common Subcategories")
        st.bar_chart(bjp_subcategory_counts)
    with col2:
        st.subheader("INC Most Common Subcategories")
        st.bar_chart(inc_subcategory_counts)

    # Display the most common summary topics
    st.subheader("Most Common Summary Topics")
    bjp_summary_topics = [x.strip() for topic in bjp_df[bjp_df['Year'].between(years[0], years[1])]['Summary_Topics'].tolist() for x in topic.split(',')]
    bjp_summary_topic_counts = pd.Series(bjp_summary_topics).value_counts()
    bjp_summary_topic_counts = bjp_summary_topic_counts.reindex(bjp_summary_topic_counts.nlargest(10).index)

    inc_summary_topics = [x.strip() for topic in inc_df[inc_df['Year'].between(years[0], years[1])]['Summary_Topics'].tolist() for x in topic.split(',')]
    inc_summary_topic_counts = pd.Series(inc_summary_topics).value_counts()
    inc_summary_topic_counts = inc_summary_topic_counts.reindex(inc_summary_topic_counts.nlargest(10).index)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("BJP Most Common Summary Topics")
        st.bar_chart(bjp_summary_topic_counts)
    with col2:
        st.subheader("INC Most Common Summary Topics")
        st.bar_chart(inc_summary_topic_counts)

    # Display the most common named entities
    st.subheader("Most Common Named Entities")
    bjp_ner_list = [ner for ner_list in bjp_df[bjp_df['Year'].between(years[0], years[1])]['NER'].tolist() for ner in eval(ner_list) if ner[0] not in stop_words + custom_stop_words]
    bjp_ner_counts = pd.Series([ner[0] for ner in bjp_ner_list]).value_counts()
    bjp_ner_counts = bjp_ner_counts.reindex(bjp_ner_counts.nlargest(10).index)

    inc_ner_list = [ner for ner_list in inc_df[inc_df['Year'].between(years[0], years[1])]['NER'].tolist() for ner in eval(ner_list) if ner[0] not in stop_words + custom_stop_words]
    inc_ner_counts = pd.Series([ner[0] for ner in inc_ner_list]).value_counts()
    inc_ner_counts = inc_ner_counts.reindex(inc_ner_counts.nlargest(10).index)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("BJP Most Common Named Entities")
        st.bar_chart(bjp_ner_counts)
    with col2:
        st.subheader("INC Most Common Named Entities")
        st.bar_chart(inc_ner_counts)

else:
    party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])
    if party == "BJP":
        df = bjp_df
    else:
        df = inc_df

    # Display the most common topics as a radar chart
    st.subheader("Most Common Topics")
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
                range=[0, max(topic_counts)]
            )),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display the most common subcategories
    st.subheader("Most Common Subcategories")
    subcategories = [x.strip() for subcategory in df[df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
    subcategory_counts = pd.Series(subcategories).value_counts()
    subcategory_counts = subcategory_counts.reindex(subcategory_counts.nlargest(10).index)
    st.bar_chart(subcategory_counts)

    # Display the most common summary topics
    st.subheader("Most Common Summary Topics")
    summary_topics = [x.strip() for topic in df[df['Year'].between(years[0], years[1])]['Summary_Topics'].tolist() for x in topic.split(',')]
    summary_topic_counts = pd.Series(summary_topics).value_counts()
    summary_topic_counts = summary_topic_counts.reindex(summary_topic_counts.nlargest(10).index)
    st.bar_chart(summary_topic_counts)

    # Display the most common named entities
    st.subheader("Most Common Named Entities")
    ner_list = [ner for ner_list in df[df['Year'].between(years[0], years[1])]['NER'].tolist() for ner in eval(ner_list) if ner[0] not in stop_words + custom_stop_words]
    ner_counts = pd.Series([ner[0] for ner in ner_list]).value_counts()
    ner_counts = ner_counts.reindex(ner_counts.nlargest(10).index)
    st.bar_chart(ner_counts)
