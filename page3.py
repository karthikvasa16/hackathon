import streamlit as st
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import networkx as nx

# Download NLTK data (if not already downloaded)
nltk.download("punkt")
nltk.download("stopwords")

def read_text(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Tokenize the sentences into words and remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [nltk.word_tokenize(sentence.lower()) for sentence in sentences]
    words = [[word for word in sentence if word.isalnum() and word not in stop_words] for sentence in words]

    return sentences, words

def sentence_similarity(sentence1, sentence2):
    # Compute cosine similarity between two sentences
    vector1 = [0] * len(word_frequencies)
    vector2 = [0] * len(word_frequencies)

    for word in sentence1:
        if word in word_frequencies:
            vector1[word_frequencies.index(word)] += 1

    for word in sentence2:
        if word in word_frequencies:
            vector2[word_frequencies.index(word)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    # Fill in the similarity matrix
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(words[i], words[j])

    return similarity_matrix

def generate_summary(text, num_sentences=3):
    sentences, words = read_text(text)
    global word_frequencies
    word_frequencies = [word for sentence in words for word in sentence]

    similarity_matrix = build_similarity_matrix(sentences, words)

    # Use NetworkX to rank sentences based on PageRank algorithm
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)

    # Sort sentences by their scores and get the top N sentences
    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)
    top_sentences = [sentence for _, sentence in ranked_sentences[:num_sentences]]

    return " ".join(top_sentences)

def main():
    st.title("Text Summarization without Transformers")

    text = st.text_area("Enter your text here:", height = 400)

    if st.button("Summarize"):
        if text:
            summary = generate_summary(text)
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter some text for summarization.")

if __name__ == "_main_":
    main()
