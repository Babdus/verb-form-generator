from scipy import stats
import numpy as np




# group_a = list of per-verb preverbed% for activity, state, frequentative
# group_b = list of per-verb preverbed% for the other 5 classes

stat, p = stats.mannwhitneyu(group_a, group_b, alternative='less')
print(f"U statistic: {stat}, p-value: {p:.4f}")