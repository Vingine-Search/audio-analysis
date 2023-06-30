
import utils as ut
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--sc_file', type=str, default=None, help='seconds file path')
parser.add_argument('--topic_file', type=str, default=None, help='topic file path')

args = parser.parse_args()
sc_file = args.sc_file
topic_file = args.topic_file

# extract file name from topic_file
file_name = topic_file.split('.')[0]
# read the topic file and return a list of topics
topics_list = ut.read_topic_file(topic_file)

# read the seconds file and return a list of words corresponding to its seoconds
seconds_list = ut.read_seconds_file(sc_file)

# compare the seconds list with the topics list and return a the starting and ending time of the topic
topics_segments = ut.compare_seconds_with_topics(seconds_list, topics_list)

# write the topics segments to the file_name.topics file
with open(file_name + '.topics', 'w') as f:
    for segment in topics_segments:
        f.write(str(segment[0]) + ' ' + str(segment[1]) + '\n')