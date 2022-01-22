"""
Analyze sd proportion for tweets belonging to top10 topics in each phase from
    1. verified vs. unverified
    2. after removing organization tweets from verified tweets: verified(human) vs. unverified
"""

import os
import pickle as pkl
import pandas as pd
from load_data import load_data
from plots import plot_lines_over_topic

HOME = './data'
df = load_data(phase='all', with_topic=True)
top10_df = df[df['topic'] < 10]

# 1. verified vs. unverified
vvsnv = top10_df.groupby(by=['phase', 'topic', 'Verified']).agg({
    "TweetID": 'count',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
vvsnv['information_sd'] = vvsnv['Information_bin'] / vvsnv['TweetID']
vvsnv['Thought_sd'] = vvsnv['Thought_bin'] / vvsnv['TweetID']
vvsnv['Feeling_sd'] = vvsnv['Feeling_bin'] / vvsnv['TweetID']
vvsnv['Intimacy_sd'] = vvsnv['Intimacy_bin'] / vvsnv['TweetID']
vvsnv['Relation_sd'] = vvsnv['Relation_bin'] / vvsnv['TweetID']

plot_labels = ['information', 'thought', 'feeling', 'intimacy', 'relation']
phase1 = vvsnv.iloc[vvsnv.index.get_level_values('phase') == 'phase1']
# load topic keywords
with open(os.path.join(HOME, 'csv_files/phase1_top50.pkl'), 'rb') as f:
    topics1 = pkl.load(f)
keywords_list1 = [[tt[0] for tt in t['keywords']] for t in topics1]
keywords_list1 = [t[:10] for t in keywords_list1]         # first 10 words for each topic
kw1 = ['\n'.join(kwl) for kwl in keywords_list1[:10]]     # top10 topics
plot_lines_over_topic(phase1, 'Verified', plot_labels, kw1,
                      os.path.join(HOME, 'figures/vvsnv_sd_proportion_top10topics_phase1.png'))

phase2 = vvsnv.iloc[vvsnv.index.get_level_values('phase') == 'phase2']
# load topic keywords
with open(os.path.join(HOME, 'csv_files/phase2_top50.pkl'), 'rb') as f:
    topics2 = pkl.load(f)
keywords_list2 = [[tt[0] for tt in t['keywords']] for t in topics2]
keywords_list2 = [t[:10] for t in keywords_list2]         # first 10 words for each topic
kw2 = ['\n'.join(kwl) for kwl in keywords_list2[:10]]     # top10 topics
plot_lines_over_topic(phase2, 'Verified', plot_labels, kw2,
                      os.path.join(HOME, 'figures/vvsnv_sd_proportion_top10topics_phase2.png'))

phase3 = vvsnv.iloc[vvsnv.index.get_level_values('phase') == 'phase3']
# load topic keywords
with open(os.path.join(HOME, 'csv_files/phase3_top50.pkl'), 'rb') as f:
    topics3 = pkl.load(f)
keywords_list3 = [[tt[0] for tt in t['keywords']] for t in topics3]
keywords_list3 = [t[:10] for t in keywords_list3]         # first 10 words for each topic
kw3 = ['\n'.join(kwl) for kwl in keywords_list3[:10]]     # top10 topics
plot_lines_over_topic(phase3, 'Verified', plot_labels, kw3,
                      os.path.join(HOME, 'figures/vvsnv_sd_proportion_top10topics_phase3.png'))

# 2. after removing organization tweets from verified tweets: verified(human) vs. unverified
no_org_df = top10_df[(top10_df['Verified'] == False) or
                     ((top10_df['Verified'] == True) and (top10_df['Organization_prob'] < 0.5))]
no_org_df = no_org_df.groupby(by=['phase', 'topic', 'Verified']).agg({
    "TweetID": 'count',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
no_org_df['information_sd'] = no_org_df['Information_bin'] / no_org_df['TweetID']
no_org_df['Thought_sd'] = no_org_df['Thought_bin'] / no_org_df['TweetID']
no_org_df['Feeling_sd'] = no_org_df['Feeling_bin'] / no_org_df['TweetID']
no_org_df['Intimacy_sd'] = no_org_df['Intimacy_bin'] / no_org_df['TweetID']
no_org_df['Relation_sd'] = no_org_df['Relation_bin'] / no_org_df['TweetID']

no_org_phase1 = no_org_df.iloc[no_org_df.index.get_level_values('phase') == 'phase1']
plot_lines_over_topic(no_org_phase1, 'Verified', plot_labels, kw1,
                      os.path.join(HOME, 'figures/humanvsnv_sd_proportion_top10topics_phase1.png'))

no_org_phase2 = no_org_df.iloc[no_org_df.index.get_level_values('phase') == 'phase2']
plot_lines_over_topic(no_org_phase2, 'Verified', plot_labels, kw2,
                      os.path.join(HOME, 'figures/humanvsnv_sd_proportion_top10topics_phase2.png'))

no_org_phase3 = no_org_df.iloc[no_org_df.index.get_level_values('phase') == 'phase3']
plot_lines_over_topic(no_org_phase3, 'Verified', plot_labels, kw3,
                      os.path.join(HOME, 'figures/humanvsnv_sd_proportion_top10topics_phase3.png'))



