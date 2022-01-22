"""
Comparing baseline sd rate and sd rate for 3 specific topics in each phase
    1. verified vs unverified (baseline: all topics)
    2. human vs organization (baseline: all topics)
    3. verified vs unverified (topic == wearing masks)
    4. human vs organization (topic == wearing masks)
    5. verified vs unverified (topic == school)
    6. human vs organization (topic == school)
    7. verified vs unverified (topic == vaccine)
    8. human vs organization (topic == vaccine)

It generates the below table:
                            Wearing masks   |   School  |   Vaccine |   General     |
phase1  |   verified    |                   |           |           |               |
                human   |                   |           |           |               |
                org     |                   |           |           |               |
            unverified  |                   |           |           |               |
phase2  |   verified    |                   |           |           |               |
                human   |                   |           |           |               |
                org     |                   |           |           |               |
            unverified  |                   |           |           |               |
phase3  |   verified    |                   |           |           |               |
                human   |                   |           |           |               |
                org     |                   |           |           |               |
            unverified  |                   |           |           |               |

"""
import os
import pickle as pkl
import pandas as pd
from load_data import load_data

HOME = './data'
df = load_data(phase='all', with_topic=True)
df['sd'] = df['Information_bin'] | df['Thought_bin'] | df['Feeling_bin'] | df['Intimacy_bin'] | df['Relation_bin']

# 1. analyze sd rate for verified vs. unverified(baseline) tweets in each phase
v_vs_nv = df.groupby(by=['phase', 'Verified']).agg({
    'TweetID': 'count',
    'sd': 'sum'
})
v_vs_nv['sd_rate'] = v_vs_nv['sd'] / v_vs_nv['TweetID']
print("analyze sd rate for verified vs. unverified(baseline) tweets in each phase")
print(v_vs_nv)

# 2. analyze sd rate for human vs. organization(baseline) tweets in each phase
verified_df = df[df['Verified'] == True]
verified_df['is_org'] = verified_df['Organization_prob'].apply(lambda x: x >= 0.5)

human_vs_org = verified_df.groupby(by=['phase', 'is_org']).agg({
    'TweetID': 'count',
    'sd': 'sum'
})
human_vs_org['sd_rate'] = human_vs_org['sd'] / human_vs_org['TweetID']
print("analyze sd rate for human vs. organization(baseline) tweets in each phase")
print(human_vs_org)

# 3. analyze sd rate for verified vs. unverified(topic=wearing masks) tweets in each phase
masks_df = df[((df['phase'] == 'phase1') and (df['topic'] == 3)) or
              ((df['phase'] == 'phase2') and (df['topic'] == 0)) or
              ((df['phase'] == 'phase3') and (df['topic'] == 0))]
masks_v_vs_nv = masks_df.groupby(by=['phase', 'Verified']).agg({
    'TweetID': 'count',
    'sd': 'sum'
})
masks_v_vs_nv['sd_rate'] = masks_v_vs_nv['sd'] / masks_v_vs_nv['TweetID']
print("analyze sd rate for verified vs. unverified(topic=wearing masks) tweets in each phase")
print(masks_v_vs_nv)

# 4. analyze sd rate for human vs. organization(topic=wearing masks) tweets in each phase
masks_verified_df = masks_df[masks_df['Verified'] == True]
masks_verified_df['is_org'] = masks_verified_df['Organization_prob'].apply(lambda x: x >= 0.5)

masks_human_vs_org = masks_verified_df.groupby(by=['phase', 'is_org']).agg({
    'TweetID': 'count',
    'sd': 'sum'
})
masks_human_vs_org['sd_rate'] = masks_human_vs_org['sd'] / masks_human_vs_org['TweetID']
print("analyze sd rate for human vs. organization(topic=wearing masks) tweets in each phase")
print(masks_human_vs_org)

# 5. analyze sd rate for verified vs unverified(topic=school) tweets in each phase
school_df = df[((df['phase'] == 'phase1') and (df['topic'] == 30)) or
               ((df['phase'] == 'phase2') and (df['topic'] == 10)) or
               ((df['phase'] == 'phase3') and (df['topic'] == 1))]
school_v_vs_nv = school_df.groupby(by=['phase', 'Verified']).agg({
    'TweetID': 'count',
    'sd': 'sum'
})
school_v_vs_nv['sd_rate'] = school_v_vs_nv['sd'] / school_v_vs_nv['TweetID']
print("analyze sd rate for verified vs. unverified(topic=school) tweets in each phase")
print(school_v_vs_nv)

# 6. analyze sd rate for human vs. organization(topic=school) tweets in each phase
school_verified_df = school_df[school_df['Verified'] == True]
school_verified_df['is_org'] = school_verified_df['Organization_prob'].apply(lambda x: x >= 0.5)

school_human_vs_org = school_verified_df.groupby(by=['phase', 'is_org']).agg({
    'TweetID': 'count',
    'sd': 'sum'
})
school_human_vs_org['sd_rate'] = school_human_vs_org['sd'] / school_human_vs_org['TweetID']
print("analyze sd rate for human vs. organization(topic=school) tweets in each phase")
print(school_human_vs_org)

# 7. analyze sd rate for verified vs. unverified(topic=vaccine) tweets in each phase
vaccine_df = df[((df['phase'] == 'phase1') and (df['topic'] == 11)) or
                ((df['phase'] == 'phase2') and (df['topic'] == 8)) or
                ((df['phase'] == 'phase3') and (df['topic'] == 2))]
vaccine_v_vs_nv = vaccine_df.groupby(by=['phase', 'Verified']).agg({
    'TweetID': 'count',
    'sd': 'sum'
})
vaccine_v_vs_nv['sd_rate'] = vaccine_v_vs_nv['sd'] / vaccine_v_vs_nv['TweetID']
print("analyze sd rate for verified vs. unverified(topic=vaccine) tweets in each phase")
print(vaccine_v_vs_nv)

# 8. analyze sd rate for human vs. organization(topic=vaccine) tweets in each phase
vaccine_verified_df = vaccine_df[vaccine_df['Verified'] == True]
vaccine_verified_df['is_org'] = vaccine_verified_df['Organization_prob'].apply(lambda x: x >= 0.5)

vaccine_human_vs_org = vaccine_verified_df.groupby(by=['phase', 'is_org']).agg({
    'TweetID': 'count',
    'sd': 'sum'
})
vaccine_human_vs_org['sd_rate'] = vaccine_human_vs_org['sd'] / vaccine_human_vs_org['TweetID']
print("analyze sd rate for human vs. organization(topic=vaccine) tweets in each phase")
print(vaccine_human_vs_org)




