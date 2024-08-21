import itertools
from definitions import counters, simple_add

# When condition_cols occurs, accumulate the number of times target_cols appears in the next draw.
# counter_type:
# - single_bn_bn: When a single B1 to B6 appears, accumulate the occurrences of B1 to B6 in the next draw.
# - single_bn_pb: When a single B1 to B6 appears, accumulate the occurrences of PB in the next draw.
# - single_bb_bn: When the BB appears, accumulate the occurrences of B1 to B6 in the next draw.
# - single_pb_bn: When the PB appears, accumulate the occurrences of B1 to B6 in the next draw.
# - single_bb_pb: When the BB appears, accumulate the occurrences of the PB in the next draw.
# - single_pb_pb: When the PB appears, accumulate the occurrences of the PB in the next draw.
# - pair_bn_bn: When a pair of B1 to B6 appears, accumulate the occurrences of B1 to B6 in the next draw.
# - pair_bn_pb: When a pair of B1 to B6 appears, accumulate the occurrences of PB in the next draw.
def calculate_counts(data, condition_cols, target_cols, counter_type):
    condition_data = data[condition_cols]
    target_data = data[target_cols].shift(-1)

    for i in range(len(data) - 1):
        if counter_type in ['pair_bn_bn', 'pair_bn_pb']:
            condition = tuple(sorted(condition_data.iloc[i]))
        else:
            condition = int(condition_data.iloc[i].item())        
        
        for target in target_data.iloc[i]:
            target = int(target)
            if isinstance(condition, tuple):
                counters[counter_type][condition][target] += 1
            else:
                counters[counter_type][(condition, target)] += 1


# Balls with higher historical occurrences are ranked first;
# for the same number of occurrences, the smaller number is ranked first.
def gen_sort(counters, bn):
    filtered_combinations = {k: v for k, v in counters.items() if k[0] == bn}
    sorted_balls = sorted(filtered_combinations.items(), key=lambda item: (-item[1], item[0][1]))
    
    return sorted_balls


# Simply add the historical occurrences of B1 to B6 and PB, and sort
def simple_add_count(last_bns, last_bb, last_pb):
    for bn in last_bns:
        sorted_single_bn_bn = gen_sort(counters['single_bn_bn'], bn)
        for (bn1, bn2), count in sorted_single_bn_bn:
            simple_add['single_bn'][bn2] += count

        sorted_single_bn_pb = gen_sort(counters['single_bn_pb'], bn)
        for (bn1, bn2), count in sorted_single_bn_pb:
            simple_add['single_pb'][bn2] += count

    sorted_single_bb_bn = gen_sort(counters['single_bb_bn'], last_bb)
    for (bn1, bn2), count in sorted_single_bb_bn:
        simple_add['single_bn'][bn2] += count

    sorted_single_pb_bn = gen_sort(counters['single_pb_bn'], last_pb)
    for (bn1, bn2), count in sorted_single_pb_bn:
        simple_add['single_bn'][bn2] += count

    sorted_single_bb_pb = gen_sort(counters['single_bb_pb'], last_bb)
    for (bn1, bn2), count in sorted_single_bb_pb:
        simple_add['single_pb'][bn2] += count

    sorted_single_pb_pb = gen_sort(counters['single_pb_pb'], last_pb)
    for (bn1, bn2), count in sorted_single_pb_pb:
        simple_add['single_pb'][bn2] += count


def print_results(last_bns, last_bb, last_pb, counter_type):
    if counter_type == 'single_bn_bn':
        for bn in last_bns:
            sorted_single_bn_bn = gen_sort(counters[counter_type], bn)
            print(f"When {bn} in B1 to B6, the probability ranking of the next ball: ")
            for (bn1, bn2), count in sorted_single_bn_bn:
                print(f"{bn2}, occurrence number: {count}")

    elif counter_type == 'single_bn_pb':
        for bn in last_bns:
            sorted_single_bn_pb = gen_sort(counters[counter_type], bn)
            print(f"When {bn} in B1 to B6, the probability ranking of the next Power Ball: ")
            for (bn1, bn2), count in sorted_single_bn_pb:
                print(f"{bn2}, occurrence number: {count}")

    elif counter_type == 'single_bb_bn':
        sorted_single_bb_bn = gen_sort(counters[counter_type], last_bb)
        print(f"When {last_bb} in BB, the probability ranking of the next ball: ")
        for (bn1, bn2), count in sorted_single_bb_bn:
            print(f"{bn2}, occurrence number: {count}")
    
    elif counter_type == 'single_pb_bn':
        sorted_single_pb_bn = gen_sort(counters[counter_type], last_pb)
        print(f"When {last_pb} in PB, the probability ranking of the next ball: ")
        for (bn1, bn2), count in sorted_single_pb_bn:
            print(f"{bn2}, occurrence number: {count}")
    
    elif counter_type == 'single_bb_pb':
        sorted_single_bb_pb = gen_sort(counters[counter_type], last_bb)
        print(f"When {last_bb} in BB, the probability ranking of the next Power Ball: ")
        for (bn1, bn2), count in sorted_single_bb_pb:
            print(f"{bn2}, occurrence number: {count}")
    
    elif counter_type == 'single_pb_pb':
        sorted_single_pb_pb = gen_sort(counters[counter_type], last_pb)
        print(f"When {last_pb} in PB, the probability ranking of the next Power Ball: ")
        for (bn1, bn2), count in sorted_single_pb_pb:
            print(f"{bn2}, occurrence number: {count}")

    elif counter_type == 'single_bn' or counter_type == 'single_pb':
        sorted_simple_add = sorted(simple_add[counter_type].items(), key=lambda x: x[1], reverse=True)
        print(f"Simply add, Next {counter_type[-2:]} historical data sorting: ")
        ranking_num = 0
        for bnpb, count in sorted_simple_add:
            ranking_num += 1
            print(f"No.{ranking_num}: {bnpb}, occurrence number: {count}")


# When pair, simply add the historical occurrences of B1 to B6 and PB, and sort
def simple_add_pair_count(last_bns):
    for last_bns_pair in list(itertools.combinations(last_bns, 2)):
        last_bns_pair = tuple(sorted(last_bns_pair))
        sorted_bn_bn_counts = dict(sorted(counters['pair_bn_bn'][last_bns_pair].items(), key=lambda item: (-item[1], item[0])))
        sorted_bn_pb_counts = dict(sorted(counters['pair_bn_pb'][last_bns_pair].items(), key=lambda item: (-item[1], item[0])))

        for key, value in sorted_bn_bn_counts.items():
            simple_add['pair_bn'][key] += value

        for key, value in sorted_bn_pb_counts.items():
            simple_add['pair_pb'][key] += value


def print_pair_results(counter_type):
    sorted_simple_add_pair = sorted(simple_add[counter_type].items(), key=lambda x: x[1], reverse=True)
    print(f"Simply add, Next {counter_type[-2:]} historical data sorting: ")
    ranking_num = 0
    for bnpb, count in sorted_simple_add_pair:
        ranking_num += 1
        print(f"No.{ranking_num}: {bnpb}, occurrence number: {count}")