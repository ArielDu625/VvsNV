"""
analyze 5 aspects' sd rate overtime(divide the time period over whole dataset into 40 buckets) on tweet level from
    1. verified vs unverified
    2. human vs organization
    3. human vs unverified
"""

import os
import pickle as pkl
import pandas as pd
from load_data import load_data
from plots import plot_lines_overtime


HOME = './data'
df = load_data(phase='all', with_topic=True)
df['TimeStamp'] = df['TimeStamp'].apply(lambda x: pd.to_datetime(x, format='%a %b %d %H:%M:%S %z %Y'))

# 1. show 5 aspects' sd rate change over time for verified and unverified tweets
n = 40  # number of periods
_, bins = pd.cut(df['TimeStamp'], bins=n, retbins=True)
bins_label = [t.strftime('%Y-%m-%d') for t in bins.to_list()]
df['TimePeriod'] = pd.cut(df['TimeStamp'], bins=n, labels=bins_label[:n])

time_df = df.groupby(by=['TimePeriod', 'Verified']).agg({
    'TweetID': 'count',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
time_df['Information_sd_rate'] = time_df['Information_bin'] / time_df['TweetID']
time_df['Thought_sd_rate'] = time_df['Thought_bin'] / time_df['TweetID']
time_df['Feeling_sd_rate'] = time_df['Feeling_bin'] / time_df['TweetID']
time_df['Intimacy_sd_rate'] = time_df['Intimacy_bin'] / time_df['TweetID']
time_df['Relation_sd_rate'] = time_df['Relation_bin'] / time_df['TweetID']

plot_lines_overtime(time_df, 'Verified', 'TimePeriod', ['verified', 'unverified'],
                    os.path.join(HOME, 'figures/vvsnv_tweet_sd_overtime.png'))

# 2. show 5 aspects' sd rate change over time for human and organization tweets
verified_df = df[df['Verified'] == True]
verified_df['is_org'] = verified_df['Organization_prob'].apply(lambda x: x >= 0.5)

human_org_df = verified_df.groupby(by=['TimePeriod', 'is_org']).agg({
    'TweetID': 'count',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
human_org_df['Information_sd_rate'] = human_org_df['Information_bin'] / human_org_df['TweetID']
human_org_df['Thought_sd_rate'] = human_org_df['Thought_bin'] / human_org_df['TweetID']
human_org_df['Feeling_sd_rate'] = human_org_df['Feeling_bin'] / human_org_df['TweetID']
human_org_df['Intimacy_sd_rate'] = human_org_df['Intimacy_bin'] / human_org_df['TweetID']
human_org_df['Relation_sd_rate'] = human_org_df['Relation_bin'] / human_org_df['TweetID']

plot_lines_overtime(human_org_df, 'is_org', 'TimePeriod', ['org', 'human'],
                    os.path.join(HOME, 'figures/humanvsorg_tweet_sd_overtime.png'))

# 3. show 5 aspects' sd rate change over time for human and unverified tweets
unverified_df = df[df['Verified'] == False]
human_df = df[(df['Verified'] == True) & (df['Organization_prob'] < 0.5)]
no_org_df = pd.concat([unverified_df, human_df])

human_unverified_df = no_org_df.groupby(by=['TimePeriod', 'Verified']).agg({
    'TweetID': 'count',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
human_unverified_df['Information_sd_rate'] = human_unverified_df['Information_bin'] / human_unverified_df['TweetID']
human_unverified_df['Thought_sd_rate'] = human_unverified_df['Thought_bin'] / human_unverified_df['TweetID']
human_unverified_df['Feeling_sd_rate'] = human_unverified_df['Feeling_bin'] / human_unverified_df['TweetID']
human_unverified_df['Intimacy_sd_rate'] = human_unverified_df['Intimacy_bin'] / human_unverified_df['TweetID']
human_unverified_df['Relation_sd_rate'] = human_unverified_df['Relation_bin'] / human_unverified_df['TweetID']

plot_lines_overtime(human_unverified_df, 'Verified', 'TimePeriod', ['verified', 'unverified'],
                    os.path.join(HOME, 'figures/humanvsnv_tweet_sd_overtime.png'))


