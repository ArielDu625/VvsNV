"""
Analyze verified and unverified tweets proportion for top10 topics in each phase
"""

import os
import pickle as pkl
from load_data import load_data
from plots import plot_cumulate_bar


HOME = './data'
df = load_data(phase='all', with_topic=True)

top10_df = df[df['topic'] < 10]
topic_df = top10_df.groupby(by=['phase', 'topic', 'Verified']).agg({
    'TweetID': 'count'
})

# phase1
phase1 = topic_df.iloc[topic_df.get_level_values('phase') == 'phase1']
plot_labels = ['verified', 'unverified']

# load topic keywords
with open(os.path.join(HOME, 'csv_files/phase1_top50.pkl'), 'rb') as f:
    topics = pkl.load(f)
keywords_list = [[tt[0] for tt in t['keywords']] for t in topics]
keywords_list = [t[:10] for t in keywords_list]         # first 10 words for each topic
kw = ['\n'.join(kwl) for kwl in keywords_list[:10]]     # top10 topics

plot_cumulate_bar(phase1, 'Verified', plot_labels,
                  kw, os.path.join(HOME, 'figures/vvsnv_proportion_top10topics_phase1.png'))

# phase2
phase2 = topic_df.iloc[topic_df.get_level_values('phase') == 'phase2']

# load topic keywords
with open(os.path.join(HOME, 'csv_files/phase2_top50.pkl'), 'rb') as f:
    topics = pkl.load(f)
keywords_list = [[tt[0] for tt in t['keywords']] for t in topics]
keywords_list = [t[:10] for t in keywords_list]         # first 10 words for each topic
kw = ['\n'.join(kwl) for kwl in keywords_list[:10]]     # top10 topics

plot_cumulate_bar(phase2, 'Verified', plot_labels,
                  kw, os.path.join(HOME, 'figures/vvsnv_proportion_top10topics_phase2.png'))

# phase3
phase3 = topic_df.iloc[topic_df.get_level_values('phase') == 'phase3']
plot_labels = ['verified', 'unverified']

# load topic keywords
with open(os.path.join(HOME, 'csv_files/phase3_top50.pkl'), 'rb') as f:
    topics = pkl.load(f)
keywords_list = [[tt[0] for tt in t['keywords']] for t in topics]
keywords_list = [t[:10] for t in keywords_list]         # first 10 words for each topic
kw = ['\n'.join(kwl) for kwl in keywords_list[:10]]     # top10 topics

plot_cumulate_bar(phase1, 'Verified', plot_labels,
                  kw, os.path.join(HOME, 'figures/vvsnv_proportion_top10topics_phase3.png'))

