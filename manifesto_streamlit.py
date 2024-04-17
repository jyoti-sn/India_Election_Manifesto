import streamlit as st
import pandas as pd

# Load the dataframes
url_bjp = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_BJP.csv'

url_inc = 'https://raw.githubusercontent.com/jyoti-sn/India_Election_Manifesto/main/FinalOutput_INC.csv'

bjp_df = pd.read_csv(url_bjp)

inc_df = pd.read_csv(url_inc)

# Create the Streamlit app
st.title("Election Manifesto Dashboard")

# Sidebar for selecting the party
party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])

# Display the selected party's dataframe
if party == "BJP":
    df = bjp_df
else:
    df = inc_df

# Display the number of years covered in the data
st.subheader(f"Number of Years: {df['Year'].nunique()}")

# Display the most common topics
st.subheader("Most Common Topics")
topics = [x.strip() for topic in df['Domains'].tolist() for x in topic.split(',')]
topic_counts = pd.Series(topics).value_counts()
st.bar_chart(topic_counts.head(10))

# Display the most common subcategories
st.subheader("Most Common Subcategories")
subcategories = [x.strip() for subcategory in df['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
subcategory_counts = pd.Series(subcategories).value_counts()
st.bar_chart(subcategory_counts.head(10))

# Display the most common named entities
st.subheader("Most Common Named Entities")
ner_list = [ner for ner_list in df['NER'].tolist() for ner in eval(ner_list)]
ner_counts = pd.Series([ner[0] for ner in ner_list]).value_counts()
st.bar_chart(ner_counts.head(10))

# Display the most common summary topics
st.subheader("Most Common Summary Topics")
summary_topics = [x.strip() for topic in df['Summary_Topics'].tolist() for x in topic.split(',')]
summary_topic_counts = pd.Series(summary_topics).value_counts()
st.bar_chart(summary_topic_counts.head(10))
