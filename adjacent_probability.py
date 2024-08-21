import pandas as pd
import itertools
from functions import calculate_counts, print_results, simple_add_count, simple_add_pair_count, print_pair_results

# Read Data
data = pd.read_csv('LottoData.csv')

# Remove rows with empty PB and then sort
data = data.dropna(subset=['PB']).sort_values('Draw', ascending=True).reset_index(drop=True)

# Columns in data
all_bn_cols = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']
bb_col = ['BB']
pb_col = ['PB']
# Each columns in all_bn_cols
bn_pairs = list(itertools.combinations(all_bn_cols, 2))


# Based on the previous draw, accumulate the occurrences of the balls in the next draw.
# Single
for col in all_bn_cols:
    calculate_counts(data, [col], all_bn_cols, 'single_bn_bn')
    calculate_counts(data, [col], pb_col, 'single_bn_pb')

calculate_counts(data, bb_col, all_bn_cols, 'single_bb_bn')
calculate_counts(data, pb_col, all_bn_cols, 'single_pb_bn')
calculate_counts(data, bb_col, pb_col, 'single_bb_pb')
calculate_counts(data, pb_col, pb_col, 'single_pb_pb')
# Pair
for pair in bn_pairs:
    calculate_counts(data, list(pair), all_bn_cols, 'pair_bn_bn')
    calculate_counts(data, list(pair), pb_col, 'pair_bn_pb')


# Last draw results
last_draw = data.iloc[-1]
last_bns = last_draw[all_bn_cols].astype(int).tolist()
last_bb = int(last_draw['BB'])
last_pb = int(last_draw['PB'])
print(f"Last Result：{last_bns}，BB：{last_bb}，PB：{last_pb}\n")


# Based on the last drawn balls, get the next historical data and sort
simple_add_count(last_bns, last_bb, last_pb)
simple_add_pair_count(last_bns)


# print_results(last_bns, last_bb, last_pb, counter_type='single_bn_bn')
# print_results(last_bns, last_bb, last_pb, counter_type='single_bn_pb')
# print_results(last_bns, last_bb, last_pb, counter_type='single_bb_bn')
# print_results(last_bns, last_bb, last_pb, counter_type='single_pb_bn')
# print_results(last_bns, last_bb, last_pb, counter_type='single_bb_pb')
# print_results(last_bns, last_bb, last_pb, counter_type='single_pb_pb')

# Print simply add results for consideration
print_results(last_bns, last_bb, last_pb, counter_type='single_bn')
print_results(last_bns, last_bb, last_pb, counter_type='single_pb')
print()
print_pair_results(counter_type='pair_bn')
print_pair_results(counter_type='pair_pb')