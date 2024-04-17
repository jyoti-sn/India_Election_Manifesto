import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import nltk
from wordcloud import WordCloud
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
stop_words = ['the', 'and', 'a', 'in', 'to', 'of', 'for']
custom_stop_words = ['Bharatiya', 'Janata', 'Party']

if compare_parties:
    # Display the most common topics as a radar chart
    st.subheader("Most Common Topics for BJP and INC from [{}] to [{}]".format(years[0], years[1]))
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
    st.subheader("Most Common Subcategories for BJP and INC from [{}] to [{}]".format(years[0], years[1]))
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
    st.subheader("Most Common Summary Topics for BJP and INC from [{}] to [{}]".format(years[0], years[1]))
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
    st.subheader("Most Common Named Entities for BJP and INC from [{}] to [{}]".format(years[0], years[1]))
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

    # Display the word clouds
    st.subheader("Word Clouds for BJP and INC from [{}] to [{}]".format(years[0], years[1]))
    col1, col2 = st.columns(2)
    with col1:
        bjp_text = ' '.join(bjp_df[bjp_df['Year'].between(years[0], years[1])]['Text'])
        bjp_wordcloud = WordCloud(stopwords=stop_words + custom_stop_words, background_color='white').generate(bjp_text)
        plt.figure(figsize=(8, 8))
        plt.imshow(bjp_wordcloud)
        plt.axis("off")
        st.subheader("BJP Word Cloud")
        st.pyplot(plt)
    with col2:
        inc_text = ' '.join(inc_df[inc_df['Year'].between(years[0], years[1])]['Text'])
        inc_wordcloud = WordCloud(stopwords=stop_words + custom_stop_words, background_color='white').generate(inc_text)
        plt.figure(figsize=(8, 8))
        plt.imshow(inc_wordcloud)
        plt.axis("off")
        st.subheader("INC Word Cloud")
        st.pyplot(plt)

    # Display the word frequency
    st.subheader("Word Frequency Comparison for BJP and INC from [{}] to [{}]".format(years[0], years[1]))
    word = st.text_input("Enter a word to search:")
    if word:
        bjp_word_count = bjp_df[bjp_df['Year'].between(years[0], years[1])]['Text'].str.contains(word, case=False).sum()
        inc_word_count = inc_df[inc_df['Year'].between(years[0], years[1])]['Text'].str.contains(word, case=False).sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(years[0], years[1] + 1, 5)), y=[bjp_word_count], mode='lines', name='BJP'))
        fig.add_trace(go.Scatter(x=list(range(years[0], years[1] + 1, 5)), y=[inc_word_count], mode='lines', name='INC'))
        fig.update_layout(title=f'Frequency of "{word}" in BJP and INC manifestos')
        st.plotly_chart(fig)

else:
    party = st.sidebar.selectbox("Select a party", ["BJP", "INC"])
    if party == "BJP":
        df = bjp_df
    else:
        df = inc_df

    # Display the most common topics as a radar chart
    st.subheader("Most Common Topics for {} from [{}] to [{}]".format(party, years[0], years[1]))
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
    st.subheader("Most Common Subcategories for {} from [{}] to [{}]".format(party, years[0], years[1]))
    subcategories = [x.strip() for subcategory in df[df['Year'].between(years[0], years[1])]['Topic_Subcategories'].tolist() for x in subcategory.split(',')]
    subcategory_counts = pd.Series(subcategories).value_counts()
    subcategory_counts = subcategory_counts.reindex(subcategory_counts.nlargest(10).index)
    st.bar_chart(subcategory_counts)

    # Display the most common summary topics
    st.subheader("Most Common Summary Topics for {} from [{}] to [{}]".format(party, years[0], years[1]))
    summary_topics = [x.strip() for topic in df[df['Year'].between(years[0], years[1])]['Summary_Topics'].tolist() for x in topic.split(',')]
    summary_topic_counts = pd.Series(summary_topics).value_counts()
    summary_topic_counts = summary_topic_counts.reindex(summary_topic_counts.nlargest(10).index)
    st.write(", ".join(summary_topic_counts.index))

    # Display the most common named entities
    st.subheader("Most Common Named Entities for {} from [{}] to [{}]".format(party, years[0], years[1]))
    ner_list = [ner for ner_list in df[df['Year'].between(years[0], years[1])]['NER'].tolist() for ner in eval(ner_list) if ner[0] not in stop_words + custom_stop_words]
    ner_counts = pd.Series([ner[0] for ner in ner_list]).value_counts()
    ner_counts = ner_counts.reindex(ner_counts.nlargest(10).index)
    st.bar_chart(ner_counts)

    # Display the word cloud
    st.subheader("Word Cloud for {} from [{}] to [{}]".format(party, years[0], years[1]))
    party_text = ' '.join(df[df['Year'].between(years[0], years[1])]['Text'])
    party_wordcloud = WordCloud(stopwords=stop_words + custom_stop_words, background_color='white').generate(party_text)
    plt.figure(figsize=(8, 8))
    plt.imshow(party_wordcloud)
    plt.axis("off")
    st.pyplot(plt)

    # Display the word frequency
    st.subheader("Word Frequency for {} from [{}] to [{}]".format(party, years[0], years[1]))
    word = st.text_input("Enter a word to search:")
    if word:
        word_count = df[df['Year'].between(years[0], years[1])]['Text'].str.contains(word, case=False).sum()
        st.write(f'The word "{word}" appears {word_count} times in the {party} manifestos from {years[0]} to {years[1]}.')
