"""
analyze 5 aspects' sd rate overtime for verified vs. unverified conversation from
    1. all topics
    2. topic = wearing masks
    3. topic = school
    4. topic = vaccine
*.   verified conversations are those initiated by verified accounts
**.  A conversation is talking about a topic(like wearing masks) if any tweet
    in this conversation is assigned to wearing masks topic
"""

import os
import pickle as pkl
import pandas as pd
from load_data import load_data
from plots import plot_lines_overtime


def to_list(x):
    return list(x)


HOME = './data'
df = load_data(phase='all', with_topic=True)
df['TimeStamp'] = df['TimeStamp'].apply(lambda x: pd.to_datetime(x, format='%a %b %d %H:%M:%S %z %Y').date())
df['TimeStamp'] = df['TimeStamp'].apply(lambda x: x.strftime('%Y-%m-%d'))

# if ParentID is None, we think itself is a parent tweet, so fill tweet's ParentID with its own TweetID
df['ParentID'].fillna(df['TweetID'], inplace=True)

# 1. all topics
con_df = df.groupby('ParentID').agg({
    'TweetID': 'count',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
con_df.reset_index(inplace=True)
con_df.rename(columns={'TweetID': 'Conversation_length'}, inplace=True)
con_df = con_df.merge(df[['TweetID', 'TimeStamp', 'Verified']], how='left', left_on='ParentID', right_on='TweetID')

time_df = con_df.groupby(by=['TimeStamp', 'Verified']).agg({
    'ParentID': 'count',
    'Conversation_length': 'sum',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
time_df.rename(columns={'ParentID': '#conversations', 'Conversation_length': '#Tweets',
                        'Information_bin': '#Information_SD',
                        'Thought_bin': '#Thought_SD',
                        'Feeling_bin': '#Feeling_SD',
                        'Intimacy_bin': '#Intimacy_SD',
                        'Relation_bin': '#Relation_SD'}, inplace=True)

time_df['Information_sd_rate'] = time_df['#Information_SD'] / time_df['#Tweets']
time_df['Thought_sd_rate'] = time_df['#Thought_SD'] / time_df['#Tweets']
time_df['Feeling_sd_rate'] = time_df['#Feeling_SD'] / time_df['#Tweets']
time_df['Intimacy_sd_rate'] = time_df['#Intimacy_SD'] / time_df['#Tweets']
time_df['Relation_sd_rate'] = time_df['#Relation_SD'] / time_df['#Tweets']

plot_labels = ['verified', 'unverified']
plot_lines_overtime(time_df, 'Verified', 'TimeStamp', plot_labels,
                    os.path.join(HOME, 'figures/vvsnv_conversation_sd_overtime.png'))

# 2. topic = wearing masks
tmp = df.groupby(by=['phase', 'ParentID']).agg({
    'TweetID': 'count',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum',
    'topic': to_list,
})
tmp.rename(columns={'TweetID': 'conversation_length', 'topic': 'topics_involved'}, inplace=True)
tmp.reset_index(inplace=True)
mask_df = tmp[((tmp['phase'] == 'phase1') and (tmp['topic'] == 3)) or
              ((tmp['phase'] == 'phase2') and (tmp['topic'] == 0)) or
              ((tmp['phase'] == 'phase3') and (tmp['topic'] == 0))]

mask_df = mask_df.merge(df[['TweetID', 'TimeStamp', 'Verified']], how='left', left_on='ParentID', right_on='TweetID')
mask_time_df = mask_df.groupby(by=['TimeStamp', 'Verified']).agg({
    'ParentID': 'count',
    'Conversation_length': 'sum',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
mask_time_df.rename(columns={'ParentID': '#conversations', 'Conversation_length': '#Tweets',
                             'Information_bin': '#Information_SD',
                             'Thought_bin': '#Thought_SD',
                             'Feeling_bin': '#Feeling_SD',
                             'Intimacy_bin': '#Intimacy_SD',
                             'Relation_bin': '#Relation_SD'}, inplace=True)

mask_time_df['Information_sd_rate'] = mask_time_df['#Information_SD'] / mask_time_df['#Tweets']
mask_time_df['Thought_sd_rate'] = mask_time_df['#Thought_SD'] / mask_time_df['#Tweets']
mask_time_df['Feeling_sd_rate'] = mask_time_df['#Feeling_SD'] / mask_time_df['#Tweets']
mask_time_df['Intimacy_sd_rate'] = mask_time_df['#Intimacy_SD'] / mask_time_df['#Tweets']
mask_time_df['Relation_sd_rate'] = mask_time_df['#Relation_SD'] / mask_time_df['#Tweets']

plot_lines_overtime(mask_time_df, 'Verified', 'TimeStamp', plot_labels,
                    os.path.join(HOME, 'figures/vvsnv_conversation_sd_masks_topic_overtime.png'))

# 3. topic = school
school_df = tmp[((tmp['phase'] == 'phase1') and (tmp['topic'] == 30)) or
                ((tmp['phase'] == 'phase2') and (tmp['topic'] == 10)) or
                ((tmp['phase'] == 'phase3') and (tmp['topic'] == 1))]

school_df = school_df.merge(df[['TweetID', 'TimeStamp', 'Verified']], how='left', left_on='ParentID',
                            right_on='TweetID')
school_time_df = school_df.groupby(by=['TimeStamp', 'Verified']).agg({
    'ParentID': 'count',
    'Conversation_length': 'sum',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
school_time_df.rename(columns={'ParentID': '#conversations', 'Conversation_length': '#Tweets',
                               'Information_bin': '#Information_SD',
                               'Thought_bin': '#Thought_SD',
                               'Feeling_bin': '#Feeling_SD',
                               'Intimacy_bin': '#Intimacy_SD',
                               'Relation_bin': '#Relation_SD'}, inplace=True)

school_time_df['Information_sd_rate'] = school_time_df['#Information_SD'] / school_time_df['#Tweets']
school_time_df['Thought_sd_rate'] = school_time_df['#Thought_SD'] / school_time_df['#Tweets']
school_time_df['Feeling_sd_rate'] = school_time_df['#Feeling_SD'] / school_time_df['#Tweets']
school_time_df['Intimacy_sd_rate'] = school_time_df['#Intimacy_SD'] / school_time_df['#Tweets']
school_time_df['Relation_sd_rate'] = school_time_df['#Relation_SD'] / school_time_df['#Tweets']

plot_lines_overtime(school_time_df, 'Verified', 'TimeStamp', plot_labels,
                    os.path.join(HOME, 'figures/vvsnv_conversation_sd_school_topic_overtime.png'))

# 4. topic = vaccine
vaccine_df = tmp[((tmp['phase'] == 'phase1') and (tmp['topic'] == 11)) or
                 ((tmp['phase'] == 'phase2') and (tmp['topic'] == 8)) or
                 ((tmp['phase'] == 'phase3') and (tmp['topic'] == 2))]

vaccine_df = vaccine_df.merge(df[['TweetID', 'TimeStamp', 'Verified']], how='left', left_on='ParentID',
                              right_on='TweetID')
vaccine_time_df = vaccine_df.groupby(by=['TimeStamp', 'Verified']).agg({
    'ParentID': 'count',
    'Conversation_length': 'sum',
    'Information_bin': 'sum',
    'Thought_bin': 'sum',
    'Feeling_bin': 'sum',
    'Intimacy_bin': 'sum',
    'Relation_bin': 'sum'
})
vaccine_time_df.rename(columns={'ParentID': '#conversations', 'Conversation_length': '#Tweets',
                                'Information_bin': '#Information_SD',
                                'Thought_bin': '#Thought_SD',
                                'Feeling_bin': '#Feeling_SD',
                                'Intimacy_bin': '#Intimacy_SD',
                                'Relation_bin': '#Relation_SD'}, inplace=True)

vaccine_time_df['Information_sd_rate'] = vaccine_time_df['#Information_SD'] / vaccine_time_df['#Tweets']
vaccine_time_df['Thought_sd_rate'] = vaccine_time_df['#Thought_SD'] / vaccine_time_df['#Tweets']
vaccine_time_df['Feeling_sd_rate'] = vaccine_time_df['#Feeling_SD'] / vaccine_time_df['#Tweets']
vaccine_time_df['Intimacy_sd_rate'] = vaccine_time_df['#Intimacy_SD'] / vaccine_time_df['#Tweets']
vaccine_time_df['Relation_sd_rate'] = vaccine_time_df['#Relation_SD'] / vaccine_time_df['#Tweets']

plot_lines_overtime(vaccine_time_df, 'Verified', 'TimeStamp', plot_labels,
                    os.path.join(HOME, 'figures/vvsnv_conversation_sd_vaccine_topic_overtime.png'))
