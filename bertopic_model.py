"""
Train BERTopic model for each phase
"""

import umap
import hdbscan
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import pickle as pkl
import logging
from .preprocess import removeKeywords


logging.basicConfig(format='%(levelname)s:%(message)s',
                    filename='./logs/phase3_model.log',
                    encoding='utf-8',
                    level=logging.DEBUG)

# 1. load data
file1 = './data/df_dyads_phase3.pkl'
file2 = './data/df_long_threads_phase3.pkl'
with open(file1, 'rb') as f1:
    df1 = pkl.load(f1)
with open(file2, 'rb') as f2:
    df2 = pkl.load(f2)
df = pd.concat([df1, df2])
docs = df['Tweet'].tolist()
docs = [removeKeywords(t) for t in docs]
logging.info('total number of tweets: %s', str(len(docs)))

# 2. modeling
umap_model = umap.UMAP(n_neighbors=90,
                       n_components=16,
                       min_dist=0.0,
                       metric='cosine',
                       low_memory=False)
hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=120)
vectorizer_model = CountVectorizer(ngram_range=(1, 3), stop_words="english")

topic_model = BERTopic(nr_topics="auto",
                       top_n_words=20,
                       umap_model=umap_model,
                       hdbscan_model=hdbscan_model,
                       vectorizer_model=vectorizer_model)
topics, _ = topic_model.fit_transform(docs)

# 3. save assigned topics
output_topics = "./results/phase3_topics.pkl"
with open(output_topics, 'wb') as f:
    pkl.dump(topics, f, protocol=pkl.HIGHEST_PROTOCOL)

# 4. save the top 50 topics and its keywords
topn = 50
top_list = []
topic_info = topic_model.get_topic_info()
topic_num = topic_info["Topic"].tolist()[1:51]
topic_size = topic_info["Count"].tolist()[1:51]
for i in range(topn):
    top_list.append({"topic": topic_num[i], "size": topic_size[i], "keywords": topic_model.get_topic(topic=i)})

output_top50 = "./results/phase3_top50.pkl"
with open(output_top50, 'wb') as f:
    pkl.dump(top_list, f, protocol=pkl.HIGHEST_PROTOCOL)

# 5. save the model
topic_model.save('./models/phase3')
