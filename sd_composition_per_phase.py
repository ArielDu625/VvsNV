"""
Analyze sd rate composition for all topics(whole dataset)/top50 topics in each phase
    1. sd rate composition for all topics
    2. sd rate composition for top50 topics
"""

import os
import pickle as pkl
import pandas as pd
from load_data import load_data
from plots import plot_pies


HOME = './data'
df = load_data(phase='all', with_topic=True)

# 1. sd rate composition for all topics
tmp = df.groupby(by=['phase', 'Verified']).agg({
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
pie_labels = ['Information', 'Thought', 'Feeling', 'Intimacy', 'Relation']
phase1 = tmp.iloc[tmp.index.get_level_values('phase') == 'phase1']
plot_pies(phase1, 'Verified', pie_labels,
          os.path.join(HOME, 'figures/sd_composition_all_phase1.png'))

phase2 = tmp.iloc[tmp.index.get_level_values('phase') == 'phase2']
plot_pies(phase2, 'Verified', pie_labels,
          os.path.join(HOME, 'figures/sd_composition_all_phase2.png'))

phase3 = tmp.iloc[tmp.index.get_level_values('phase') == 'phase3']
plot_pies(phase3, 'Verified', pie_labels,
          os.path.join(HOME, 'figures/sd_composition_all_phase3.png'))

# 2. sd rate composition for top50 topics
top50_df = df[df['topic'] < 50]
top50_tmp = top50_df.groupby(by=['phase', 'Verified']).agg({
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
top50_phase1 = top50_tmp.iloc[top50_tmp.index.get_level_values('phase') == 'phase1']
plot_pies(top50_phase1, 'Verified', pie_labels,
          os.path.join(HOME, 'figures/sd_composition_top50_phase1.png'))

top50_phase2 = top50_tmp.iloc[top50_tmp.index.get_level_values('phase') == 'phase2']
plot_pies(top50_phase2, 'Verified', pie_labels,
          os.path.join(HOME, 'figures/sd_composition_top50_phase2.png'))

top50_phase3 = top50_tmp.iloc[top50_tmp.index.get_level_values('phase') == 'phase3']
plot_pies(top50_phase3, 'Verified', pie_labels,
          os.path.join(HOME, 'figures/sd_composition_top50_phase3.png'))



