import re
import numpy as np
# this function reads an intervals file and returns a list of tuples
# each tuple contains the start and end time of a segment
def read_intervals_file(intervals_file):
    intervals = []
    with open(intervals_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            m = re.match(r'^(\d+)\s+(\d+)$', line)
            if m is None:
                raise RuntimeError("Error parsing intervals file {0}".format(intervals_file))
            intervals.append((int(m.group(1)), int(m.group(2))))
    return intervals

# this function takes intervals and a 2D numpy array of features
# and returns a list of 2D numpy arrays of features, one for each segment
def split_features(intervals, feat):
    feat_list = np.zeros((feat.shape[0], len(intervals)))
    for idx, (start, end) in enumerate(intervals):
        interval = np.mean(feat[:, start* 98:end * 98], axis=1)
        feat_list[:, idx] = interval    
    return feat_list