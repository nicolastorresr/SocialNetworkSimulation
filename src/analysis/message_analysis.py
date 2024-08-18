from collections import Counter
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def analyze_sentiment(message):
    positive_words = set(['good', 'great', 'excellent', 'amazing', 'wonderful'])
    negative_words = set(['bad', 'terrible', 'awful', 'horrible', 'poor'])
    words = message.lower().split()
    sentiment = sum(1 for word in words if word in positive_words) - sum(1 for word in words if word in negative_words)
    return sentiment

def extract_topics(messages, num_topics=5):
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform(messages)
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(doc_term_matrix)
    
    topics = []
    feature_names = vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
        topics.append(f"Topic {topic_idx}: {', '.join(top_words)}")
    return topics

def track_message_spread(network, message_id):
    spread = {0: 1}  # Time step 0: original message
    for time_step, agent in enumerate(network.agents.values(), 1):
        if any(message_id in msg for msg in agent.messages):
            spread[time_step] = spread.get(time_step, 0) + 1
    return spread
