import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

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
stop_words = set(STOPWORDS)
custom_stop_words = ['Bharatiya', 'Janata', 'Party']
all_stop_words = stop_words.union(custom_stop_words)

if compare_parties:
    # Display the most common topics as radar charts
    st.subheader("Most Common Topics for BJP and INC")
    st.write("This section shows the top 10 most common topics for BJP and INC.")

    bjp_topics = [x.strip() for topic in bjp_df[bjp_df['Year'].between(years[0], years[1])]['Domains'].tolist() for x in topic.split(',')]
    bjp_topic_counts = pd.Series(bjp_topics).value_counts()
    bjp_topic_counts = bjp_topic_counts.reindex(bjp_topic_counts.nlargest(10).index)

    inc_topics = [x.strip() for topic in inc_df[inc_df['Year'].between(years[0], years[1])]['Domains'].tolist() for x in topic.split(',')]
    inc_topic_counts = pd.Series(inc_topics).value_counts()
    inc_topic_counts = inc_topic_counts.reindex(inc_topic_counts.nlargest(10).index)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.set_title("BJP Most Common Topics")
    ax1.set_theta_direction(-1)
    ax1.set_theta_zero_location('N')
    ax1.plot(bjp_topic_counts.index, bjp_topic_counts)
    ax1.fill(bjp_topic_counts.index, bjp_topic_counts, alpha=0.2)
    ax2.set_title("INC Most Common Topics")
    ax2.set_theta_direction(-1)
    ax2.set_theta_zero_location('N')
    ax2.plot(inc_topic_counts.index, inc_topic_counts)
    ax2.fill(inc_topic_counts.index, inc_topic_counts, alpha=0.2)
    st.pyplot(fig)

    # Display the most common subcategories
    st.subheader("Most Common Subcategories for BJP and INC")
    st.write("This section shows the top 10 most common subcategories for BJP and INC.")

    bjp_subcategories = [x.strip() for subcategory in bjp_df[bjp_df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
    bjp_subcategory_counts = pd.Series(bjp_subcategories).value_counts()
    bjp_subcategory_counts = bjp_subcategory_counts.reindex(bjp_subcategory_counts.nlargest(10).index)

    inc_subcategories = [x.strip() for subcategory in inc_df[inc_df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
    inc_subcategory_counts = pd.Series(inc_subcategories).value_counts()
    inc_subcategory_counts = inc_subcategory_counts.reindex(inc_subcategory_counts.nlargest(10).index)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("BJP Most Common Subcategories")
        st.bar_chart(bjp_subcategory_counts, horizontal=True)
    with col2:
        st.subheader("INC Most Common Subcategories")
        st.bar_chart(inc_subcategory_counts, horizontal=True)

    # Display the most common summary topics
    st.subheader("Most Common Summary Topics for BJP and INC")
    st.write("This section shows the top 10 most common summary topics for BJP and INC.")

    bjp_summary_topics = [x.strip() for topic in bjp_df[bjp_df['Year'].between(years[0], years[1])]['Summary_Topics'].tolist() for x in topic.split(',')]
    bjp_summary_topic_counts = pd.Series(bjp_summary_topics).value_counts()
    bjp_summary_topic_counts = bjp_summary_topic_counts.reindex(bjp_summary_topic_counts.nlargest(10).index)

    inc_summary_topics = [x.strip() for topic in inc_df[inc_df['Year'].between(years[0], years[1])]['Summary_Topics'].tolist() for x in topic.split(',')]
    inc_summary_topic_counts = pd.Series(inc_summary_topics).value_counts()
    inc_summary_topic_counts = inc_summary_topic_counts.reindex(inc_summary_topic_counts.nlargest(10).index)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("BJP Most Common Summary Topics")
        st.write(", ".join(bjp_summary_topic_counts.index))
    with col2:
        st.subheader("INC Most Common Summary Topics")
        st.write(", ".join(inc_summary_topic_counts.index))

    # Display the most common named entities
    st.subheader("Most Common Named Entities for BJP and INC")
    st.write("This section shows the top 10 most common named entities for BJP and INC.")

    bjp_ner_list = [ner for ner_list in bjp_df[bjp_df['Year'].between(years[0], years[1])]['NER'].tolist() for ner in eval(ner_list) if ner[0] not in all_stop_words]
    bjp_ner_counts = pd.Series([ner[0] for ner in bjp_ner_list]).value_counts()
    bjp_ner_counts = bjp_ner_counts.reindex(bjp_ner_counts.nlargest(10).index)

    inc_ner_list = [ner for ner_list in inc_df[inc_df['Year'].between(years[0], years[1])]['NER'].tolist() for ner in eval(ner_list) if ner[0] not in all_stop_words]
    inc_ner_counts = pd.Series([ner[0] for ner in inc_ner_list]).value_counts()
    inc_ner_counts = inc_ner_counts.reindex(inc_ner_counts.nlargest(10).index)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Most Common Named Entities for BJP in {years[0]} - {years[1]}")
        st.bar_chart(bjp_ner_counts)
    with col2:
        st.subheader(f"Most Common Named Entities for INC in {years[0]} - {years[1]}")
        st.bar_chart(inc_ner_counts)

    # Display the word clouds
    st.subheader("Word Clouds for BJP and INC")
    st.write("This section shows the word clouds for BJP and INC based on the 'Text' column.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"BJP Word Cloud for {years[0]} - {years[1]}")
        bjp_text = ' '.join(bjp_df[bjp_df['Year'].between(years[0], years[1])]['Text'])
        bjp_wordcloud = WordCloud(stopwords=all_stop_words, background_color='white', width=800, height=400).generate(bjp_text)
        plt.figure(figsize=(8, 4))
        plt.imshow(bjp_wordcloud)
        plt.axis("off")
        st.pyplot(plt.gcf())
    with col2:
        st.subheader(f"INC Word Cloud for {years[0]} - {years[1]}")
        inc_text = ' '.join(inc_df[inc_df['Year'].between(years[0], years[1])]['Text'])
        inc_wordcloud = WordCloud(stopwords=all_stop_words, background_color='white', width=800, height=400).generate(inc_text)
        plt.figure(figsize=(8, 4))
        plt.imshow(inc_wordcloud)
        plt.axis("off")
        st.pyplot(plt.gcf())

else:
    party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])
    if party == "BJP":
        df = bjp_df
    else:
        df = inc_df

    # Display the most common topics as a radar chart
    st.subheader(f"Most Common Topics for {party} in {years[0]} - {years[1]}")
    st.write("This section shows the top 10 most common topics for the selected party and years.")

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
    st.subheader(f"Most Common Subcategories for {party} in {years[0]} - {years[1]}")
    st.write("This section shows the top 10 most common subcategories for the selected party and years.")

    subcategories = [x.strip() for subcategory in df[df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
    subcategory_counts = pd.Series(subcategories).value_counts()
    subcategory_counts = subcategory_counts.reindex(subcategory_counts.nlargest(10).index)
    st.bar_chart(subcategory_counts, horizontal=True)

    # Display the most common summary topics
    st.subheader(f"Most Common Summary Topics for {party} in {years[0]} - {years[1]}")
    st.write("This section shows the top 10 most common summary topics for the selected party and years.")

    summary_topics = [x.strip() for topic in df[df['Year'].between(years[0], years[1])]['Summary_Topics'].tolist() for x in topic.split(',')]
    summary_topic_counts = pd.Series(summary_topics).value_counts()
    summary_topic_counts = summary_topic_counts.reindex(summary_topic_counts.nlargest(10).index)
    st.write(", ".join(summary_topic_counts.index))

    # Display the most common named entities
    st.subheader(f"Most Common Named Entities for {party} in {years[0]} - {years[1]}")
    st.write("This section shows the top 10 most common named entities for the selected party and years.")

    ner_list = [ner for ner_list in df[df['Year'].between(years[0], years[1])]['NER'].tolist() for ner in eval(ner_list) if ner[0] not in all_stop_words]
    ner_counts = pd.Series([ner[0] for ner in ner_list]).value_counts()
    ner_counts = ner_counts.reindex(ner_counts.nlargest(10).index)
    st.bar_chart(ner_counts)

    # Display the word cloud
    st.subheader(f"Word Cloud for {party} in {years[0]} - {years[1]}")
    st.write("This section shows the word cloud for the selected party and years based on the 'Text' column.")

    text = ' '.join(df[df['Year'].between(years[0], years[1])]['Text'])
    wordcloud = WordCloud(stopwords=all_stop_words, background_color='white', width=800, height=400).generate(text)
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(plt.gcf())
