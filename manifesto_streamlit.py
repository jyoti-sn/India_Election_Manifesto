import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

# Load the dataframes
url_bjp = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_BJP.csv'

url_inc = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_INC.csv'

bjp_df = pd.read_csv(url_bjp)

inc_df = pd.read_csv(url_inc)

# Create the Streamlit app
st.title("India Election Manifesto Dashboard: 2004-2024")

# Sidebar for selecting the party and year
party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])
if party == "BJP":
    df = bjp_df
else:
    df = inc_df

year_filter = st.sidebar.multiselect("Select year(s)", df['Year'].unique(), default=df['Year'].unique())
all_years = st.sidebar.checkbox("Show data for all years")
if all_years:
    year_filter = df['Year'].unique()

# Display the number of years covered in the data
st.subheader(f"Number of Years: {len(year_filter)}")

# Display the most common topics as a radar chart
st.subheader("Most Common Topics")
topics = [x.strip() for topic in df['Domains'].tolist() for x in topic.split(',')]
topic_counts = pd.Series(topics).value_counts()
topic_counts = topic_counts.reindex(topic_counts.nlargest(10).index)
st.radar_chart(topic_counts)

# Display the most common subcategories
st.subheader("Most Common Subcategories")
subcategories = [x.strip() for subcategory in df['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
subcategory_counts = pd.Series(subcategories).value_counts()
subcategory_counts = subcategory_counts.reindex(subcategory_counts.nlargest(10).index)
st.bar_chart(subcategory_counts)

# Display the most common named entities
st.subheader("Most Common Named Entities")
stop_words = ['the', 'and', 'a', 'in', 'to', 'of', 'for']
custom_stop_words = ['Bharatiya', 'Janata', 'Party']
ner_list = [ner for ner_list in df['NER'].tolist() for ner in eval(ner_list) if ner[0] not in stop_words + custom_stop_words]
ner_counts = pd.Series([ner[0] for ner in ner_list]).value_counts()
st.bar_chart(ner_counts.head(10))

# Display the most common summary topics
st.subheader("Most Common Summary Topics")
summary_topics = [x.strip() for topic in df['Summary_Topics'].tolist() for x in topic.split(',')]
summary_topic_counts = pd.Series(summary_topics).value_counts()
summary_topic_counts = summary_topic_counts.reindex(summary_topic_counts.nlargest(10).index)
st.bar_chart(summary_topic_counts)

# Compare BJP and INC
if st.sidebar.checkbox("Compare BJP and INC"):
    compare_all = st.sidebar.checkbox("Compare all years")
    if compare_all:
        bjp_topics = [x.strip() for topic in bjp_df['Domains'].tolist() for x in topic.split(',')]
        bjp_topic_counts = pd.Series(bjp_topics).value_counts()
        bjp_topic_counts = bjp_topic_counts.reindex(bjp_topic_counts.nlargest(10).index)

        inc_topics = [x.strip() for topic in inc_df['Domains'].tolist() for x in topic.split(',')]
        inc_topic_counts = pd.Series(inc_topics).value_counts()
        inc_topic_counts = inc_topic_counts.reindex(inc_topic_counts.nlargest(10).index)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("BJP Most Common Topics")
            st.bar_chart(bjp_topic_counts)
        with col2:
            st.subheader("INC Most Common Topics")
            st.bar_chart(inc_topic_counts)

        bjp_subcategories = [x.strip() for subcategory in bjp_df['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
        bjp_subcategory_counts = pd.Series(bjp_subcategories).value_counts()
        bjp_subcategory_counts = bjp_subcategory_counts.reindex(bjp_subcategory_counts.nlargest(10).index)

        inc_subcategories = [x.strip() for subcategory in inc_df['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
        inc_subcategory_counts = pd.Series(inc_subcategories).value_counts()
        inc_subcategory_counts = inc_subcategory_counts.reindex(inc_subcategory_counts.nlargest(10).index)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("BJP Most Common Subcategories")
            st.bar_chart(bjp_subcategory_counts)
        with col2:
            st.subheader("INC Most Common Subcategories")
            st.bar_chart(inc_subcategory_counts)
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("BJP Most Common Topics")
            bjp_topics = [x.strip() for topic in bjp_df[bjp_df['Year'].isin(year_filter)]['Domains'].tolist() for x in topic.split(',')]
            bjp_topic_counts = pd.Series(bjp_topics).value_counts()
            bjp_topic_counts = bjp_topic_counts.reindex(bjp_topic_counts.nlargest(10).index)
            st.bar_chart(bjp_topic_counts)
        with col2:
            st.subheader("INC Most Common Topics")
            inc_topics = [x.strip() for topic in inc_df[inc_df['Year'].isin(year_filter)]['Domains'].tolist() for x in topic.split(',')]
            inc_topic_counts = pd.Series(inc_topics).value_counts()
            inc_topic_counts = inc_topic_counts.reindex(inc_topic_counts.nlargest(10).index)
            st.bar_chart(inc_topic_counts)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("BJP Most Common Subcategories")
            bjp_subcategories = [x.strip() for subcategory in bjp_df[bjp_df['Year'].isin(year_filter)]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
            bjp_subcategory_counts = pd.Series(bjp_subcategories).value_counts()
            bjp_subcategory_counts = bjp_subcategory_counts.reindex(bjp_subcategory_counts.nlargest(10).index)
            st.bar_chart(bjp_subcategory_counts)
        with col2:
            st.subheader("INC Most Common Subcategories")
            inc_subcategories = [x.strip() for subcategory in inc_df[inc_df['Year'].isin(year_filter)]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
            inc_subcategory_counts = pd.Series(inc_subcategories).value_counts()
            inc_subcategory_counts = inc_subcategory_counts.reindex(inc_subcategory_counts.nlargest(10).index)
            st.bar_chart(inc_subcategory_counts)
