import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

MAPPING = {
    'Verified': 'Unverified',
}


def plot_lines_over_topic(data: pd.DataFrame, dimension: str,
                          labels: list[str], topic_keywords: list[str], filepath: str) -> None:
    assert dimension in data.index.names
    true_df = data.iloc[data.index.get_level_values(dimension) == True]
    false_df = data.iloc[data.index.get_level_values(dimension) == False]
    true_label = [dimension + " " + label for label in labels]
    false_dimension = MAPPING[dimension]
    false_label = [false_dimension + " " + label for label in labels]

    x_axis = np.arange(len(topic_keywords))
    fig, ax = plt.subplots(figsize=(30, 10))
    ax.plot(x_axis, true_df['information_sd'].tolist(), 'b-', label=true_label[0])
    ax.plot(x_axis, false_df['information_sd'].tolist(), 'b--', label=false_label[0])
    ax.plot(x_axis, true_df['Thought_sd'].tolist(), 'g-', label=true_label[1])
    ax.plot(x_axis, false_df['Thought_sd'].tolist(), 'g--', label=false_label[1])
    ax.plot(x_axis, true_df['Feeling_sd'].tolist(), 'r-', label=true_label[2])
    ax.plot(x_axis, false_df['Feeling_sd'].tolist(), 'r--', label=false_label[2])
    ax.plot(x_axis, true_df['Intimacy_sd'].tolist(), 'c-', label=true_label[3])
    ax.plot(x_axis, false_df['Intimacy_sd'].tolist(), 'c--', label=false_label[3])
    ax.plot(x_axis, true_df['Relation_sd'].tolist(), 'm-', label=true_label[4])
    ax.plot(x_axis, false_df['Relation_sd'].tolist(), 'm--', label=false_label[4])

    ax.set_ylabel("sd proportion")
    ax.legend(loc='upper right')
    plt.xticks(x_axis, topic_keywords)
    plt.xlabel("Topics")
    plt.savefig(filepath)


def plot_cumulate_bar(data: pd.DataFrame, dimension: str,
                      labels: list[str], topic_keywords: list[str], filepath: str) -> None:
    assert dimension in data.index.names

    true_df = data.iloc[data.index.get_level_values(dimension) == True]
    false_df = data.iloc[data.index.get_level_values(dimension) == False]

    x_axis = np.arange(len(topic_keywords))
    total = [i + j for i, j in zip(true_df['TweetID'], false_df['TweetID'])]
    true_percentage = [i / j for i, j in zip(true_df['TweetID'], total)]
    false_percentage = [i / j for i, j in zip(false_df['TweetID'], total)]

    fig, ax = plt.subplots(figsize=(20, 10))
    barWidth = 0.3
    ax.bar(x_axis, false_percentage, edgecolor='white', color='#ff7f0e', width=barWidth, label=labels[1])
    ax.bar(x_axis, true_percentage, bottom=false_percentage, edgecolor='white', color='#2ca02c', width=barWidth,
           label=labels[0])
    ax.legend(loc='upper right', fontsize=15)

    plt.xticks(x_axis, topic_keywords, fontsize=15)
    plt.xlabel("Topics", fontsize=15)
    plt.ylabel('Percentage', fontsize=15)
    plt.savefig(filepath)


def plot_pies(data: pd.DataFrame, dimension: str, labels: list[str], filepath: str) -> None:
    assert dimension in data.index.names

    true_df = np.array(data.iloc[data.index.get_level_values(dimension) == True])
    false_df = np.array(data.iloc[data.index.get_level_values(dimension) == False])
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    ax[0].pie(true_df,
              labels=labels,
              autopct='%.2f%%')
    ax[0].set_title(f'Percentage of different types of SD for {dimension} = True')

    ax[1].pie(false_df,
              labels=labels,
              autopct='%.2f%%')
    ax[1].set_title(f'Percentage of different types of SD for {dimension} = False')

    plt.savefig(filepath)


def plot_lines_overtime(data: pd.DataFrame, dimension: str, x_dimension: str,
                        labels: list[str], filepath: str) -> None:
    assert dimension in data.index.names
    assert x_dimension in data.index.names

    true_df = data.iloc[data.index.get_level_values(dimension) == True]
    false_df = data.iloc[data.index.get_level_values(dimension) == False]

    x = list(set(data.index.get_level_values(x_dimension)))
    x.sort()
    x_axis = np.arange(len(x))

    fig, axs = plt.subplots(5, figsize=(30, 30))
    axs[0].plot(x_axis, true_df['Information_sd_rate'].tolist(), label=labels[0])
    axs[0].plot(x_axis, false_df['Information_sd_rate'].tolist(), label=labels[1])
    axs[0].set_title('information self-disclosure')

    axs[1].plot(x_axis, true_df['Thought_sd_rate'].tolist(), label=labels[0])
    axs[1].plot(x_axis, false_df['Thought_sd_rate'].tolist(), label=labels[1])
    axs[1].set_title('thought self-disclosure rate')

    axs[2].plot(x_axis, true_df['Feeling_sd_rate'].tolist(), label=labels[0])
    axs[2].plot(x_axis, false_df['Feeling_sd_rate'].tolist(), label=labels[1])
    axs[2].set_title('feeling self-disclosure rate')

    axs[3].plot(x_axis, true_df['Intimacy_sd_rate'].tolist(), label=labels[0])
    axs[3].plot(x_axis, false_df['Intimacy_sd_rate'].tolist(), label=labels[1])
    axs[3].set_title('intimacy self-disclosure rate')

    axs[4].plot(x_axis, true_df['Relation_sd_rate'].tolist(), label=labels[0])
    axs[4].plot(x_axis, false_df['Relation_sd_rate'].tolist(), label=labels[1])
    axs[4].set_title('relation self-disclosure rate')

    for ax in axs.flat:
        ax.axvline(x=8.8, ymin=0, ymax=1, color='black', ls='--')
        ax.axvline(x=29.2, ymin=0, ymax=1, color='black', ls='--')
        ax.set_xticks(x_axis)
        ax.set_xticklabels(x, rotation=70)
        ax.set(ylabel='sd rate')
        ax.legend(loc='upper right')

    for ax in axs.flat:
        ax.label_outer()

    plt.savefig(filepath)


