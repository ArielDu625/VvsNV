"""
find overlapping top topics shared by all three phases
"""

import pickle as pkl
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt


output_dir = './data/csv_files'
with open(os.path.join(output_dir, 'phase1_top50_topic_embeddings.pkl'), 'rb') as f:
    topic_embeddings1 = pkl.load(f)
with open(os.path.join(output_dir, 'phase2_top50_topic_embeddings.pkl'), 'rb') as f:
    topic_embeddings2 = pkl.load(f)
with open(os.path.join(output_dir, 'phase3_top50_topic_embeddings.pkl'), 'rb') as f:
    topic_embeddings3 = pkl.load(f)


with open(os.path.join(output_dir, 'phase1_top50.pkl'), 'rb') as f:
    phase1_top50 = pkl.load(f)
with open(os.path.join(output_dir, 'phase2_top50.pkl'), 'rb') as f:
    phase2_top50 = pkl.load(f)
with open(os.path.join(output_dir, 'phase3_top50.pkl'), 'rb') as f:
    phase3_top50 = pkl.load(f)

tembd1 = np.array(topic_embeddings1)
tembd2 = np.array(topic_embeddings2)
tembd3 = np.array(topic_embeddings3)

sim12 = cosine_similarity(tembd1, tembd2)
sim23 = cosine_similarity(tembd2, tembd3)
sim13 = cosine_similarity(tembd1, tembd3)
print(sim12.shape)
print(sim23.shape)
print(sim13.shape)


phase1_top50_dict = {}
for d in phase1_top50:
    phase1_top50_dict[d['topic']] = d

phase2_top50_dict = {}
for d in phase2_top50:
    phase2_top50_dict[d['topic']] = d

phase3_top50_dict = {}
for i, d in enumerate(phase3_top50):
    phase3_top50_dict[i] = d

sim12b = sim12 > 0.8
idx1, idx2 = np.where(sim12b)

sim23b = sim23 > 0.8
idx22, idx3 = np.where(sim23b)

mapping12 = {}
n12 = len(idx1)
for i in range(n12):
    if idx1[i] not in mapping12:
        mapping12[idx1[i]] = [idx2[i]]
    else:
        mapping12[idx1[i]] += [idx2[i]]

mapping23 = {}
n23 = len(idx22)
for i in range(n23):
    if idx22[i] not in mapping23:
        mapping23[idx22[i]] = [idx3[i]]
    else:
        mapping23[idx22[i]] += [idx3[i]]
print(mapping12)
print(mapping23)

p1size = []
p2size = []
p3size = []
topic_words = []

for k, v in mapping12.items():
    # print(f"k={k}")
    # print(f"v={v}")

    p1size.append(phase1_top50_dict[k]['size'])
    w = phase1_top50_dict[k]['keywords']

    s2 = 0
    for i in v:
        s2 += phase2_top50_dict[i]['size']
        w.extend(phase2_top50_dict[i]['keywords'])
    p2size.append(s2)

    s3 = 0
    for i in v:
        t3 = mapping23.get(i)
        if t3:
            for j in t3:
                s3 += phase3_top50_dict[j]['size']
                w.extend(phase3_top50_dict[j]['keywords'])
    if s3 == 0:
        p1size.pop()
        p2size.pop()
        continue

    p3size.append(s3)
    # sort by probability, use top 20 words as keywords
    w.sort(key=lambda x: -x[1])
    kw = []
    for val in w:
        if len(kw) >= 2:
            break
        if val[0] in kw:
            continue
        kw.append(val[0])
    topic_words.append(kw)

print(len(p1size))
assert len(p1size) == len(p2size)
assert len(p2size) == len(p3size)
assert len(p1size) == len(topic_words)

print(p1size)
print(p2size)
print(p3size)
print(topic_words)


n = len(p1size)
width = 2
x_axis = np.arange(n)*10-width
x = ["\n".join(i) for i in topic_words]

# plt.figure(dpi=1200)
fig, ax = plt.subplots(figsize=(65, 15))
ax.bar(x_axis-width, p1size, width, label='phase1')
ax.bar(x_axis, p2size, width, label='phase2')
ax.bar(x_axis+width, p3size, width, label='phase3')
ax.set_ylabel("topic size", fontsize=50)
ax.tick_params(axis='y', labelsize=50)
plt.xticks(x_axis, x, fontsize=35)
plt.legend(loc='upper right', fontsize=50)

plt.savefig(os.path.join(output_dir, 'TopicsOverThreePhases.png'))
