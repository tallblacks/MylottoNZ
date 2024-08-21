from collections import defaultdict

# Initialize counters
counters = {
    'single_bn_bn': defaultdict(int),
    'single_bb_bn': defaultdict(int),
    'single_pb_bn': defaultdict(int),
    'single_bn_pb': defaultdict(int),
    'single_bb_pb': defaultdict(int),
    'single_pb_pb': defaultdict(int),
    'pair_bn_bn': defaultdict(lambda: defaultdict(int)),
    'pair_bn_pb': defaultdict(lambda: defaultdict(int)),
}

# Initialize simple add counters
simple_add = {
    'single_bn': defaultdict(int),
    'single_pb': defaultdict(int),
    'pair_bn': defaultdict(int),
    'pair_pb': defaultdict(int)
}