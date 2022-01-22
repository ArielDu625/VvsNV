"""
Load data
"""
import os
import pickle as pkl
import pandas as pd


def load_data(phase='all', with_topic=True):
    """

    :param phase: str, default='all', value can be 'phase1', 'phase2', 'phase3', 'all'
    :param with_topic: bool, default=True
    :return: pd.DataFrame
    """
    HOME = './data'

    if phase == 'all':
        # load data in phase1
        filename11 = os.path.join(HOME, "df_dyads_phase1.pkl")
        filename12 = os.path.join(HOME, "df_long_threads_phase1.pkl")

        with open(filename11, 'rb') as f:
            tmp11 = pkl.load(f)
        with open(filename12, 'rb') as f:
            tmp12 = pkl.load(f)
        df1 = pd.concat([tmp11, tmp12])
        df1['phase'] = 'phase1'

        # load data in phase2
        filename21 = os.path.join(HOME, "df_dyads_phase2.pkl")
        filename22 = os.path.join(HOME, "df_long_threads_phase2.pkl")

        with open(filename21, 'rb') as f:
            tmp21 = pkl.load(f)
        with open(filename22, 'rb') as f:
            tmp22 = pkl.load(f)
        df2 = pd.concat([tmp21, tmp22])
        df2['phase'] = 'phase2'

        # load data in phase3
        filename31 = os.path.join(HOME, "df_dyads_phase3.pkl")
        filename32 = os.path.join(HOME, "df_long_threads_phase3.pkl")

        with open(filename31, 'rb') as f:
            tmp31 = pkl.load(f)
        with open(filename32, 'rb') as f:
            tmp32 = pkl.load(f)
        df3 = pd.concat([tmp31, tmp32])
        df3['phase'] = 'phase3'

        if with_topic:
            with open(os.path.join(HOME, 'csv_files/phase1_topic_labels.pkl'), 'rb') as f:
                label1 = pkl.load(f)

            assert len(df1) == len(label1)
            df1['topic'] = label1

            with open(os.path.join(HOME, 'csv_files/phase2_topic_labels.pkl'), 'rb') as f:
                label2 = pkl.load(f)

            assert len(df2) == len(label2)
            df2['topic'] = label2

            with open(os.path.join(HOME, 'csv_files/phase3_topic_labels.pkl'), 'rb') as f:
                label3 = pkl.load(f)

            assert len(df3) == len(label3)
            df3['topic'] = label3

        df = pd.concat([df1, df2, df3])

    else:
        filename1 = os.path.join(HOME, "df_dyads_" + phase + ".pkl")
        filename2 = os.path.join(HOME, "df_long_threads_" + phase + ".pkl")
        with open(filename1, 'rb') as f:
            tmp1 = pkl.load(f)
        with open(filename2, 'rb') as f:
            tmp2 = pkl.load(f)
        df = pd.concat([tmp1, tmp2])
        df['phase'] = phase

        if with_topic:
            with open(os.path.join(HOME, 'csv_files/' + phase + '_topic_labels.pkl'), 'rb') as f:
                label = pkl.load(f)
            assert len(df) == len(label)
            df['topic'] = label

    return df


