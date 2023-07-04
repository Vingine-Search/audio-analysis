import os
import argparse

# this fuction is used to read the topic file and return a list of topics
def read_topic_file(topic_file):
    topic_list = []
    # read the topic file and split it on the new line
    with open(topic_file, 'r') as f:
        topics = f.read().split('\n\n')
    # for each topic in the topics list
    for topic in topics:
        # if the topic is not empty
        if topic != '':
            words = [0 for _ in topic.split()]
            # Mark the last word as a topic segment
            words[-1] = 1
            topic_list.extend(words)
    # return the topic list
    return topic_list

# this function reads the seconds file and returns a list of words corresponding to its seoconds
def read_seconds_file(seconds_file):
    seconds_list = []
    # read the seconds file and split it on the new line
    with open(seconds_file, 'r') as f:
        seconds = f.read().split('\n')
    # for each second in the seconds 
    for i, second in enumerate(seconds):
        words = [i for _ in second.split()]
        seconds_list.extend(words)
    # return the words list
    return seconds_list

# this function is used to compare the seconds list with the topics list 
# and return a the starting and ending time of the topic
def compare_seconds_with_topics(seconds_list, topic_list):
    # for each topic in the topic list
    split_secs = []
    for tw, ts in zip(topic_list, seconds_list):
        if tw == 1:
            split_secs.append(ts)
    last_sec = 0
    range_split_secs = []
    for sec in split_secs:
        range_split_secs.append((last_sec, sec))
        last_sec = sec
    return range_split_secs

def main(topic_file, sc_file):
    # extract file name from topic_file
    file_name, _ = os.path.splitext(topic_file)

    # read the topic file and return a list of topics
    topics_list = read_topic_file(topic_file)

    # read the seconds file and return a list of words corresponding to its seoconds
    seconds_list = read_seconds_file(sc_file)

    # compare the seconds list with the topics list and return a the starting and ending time of the topic
    topics_segments = compare_seconds_with_topics(seconds_list, topics_list)

    # write the topics segments to the file_name.topics file
    with open(file_name + '.bounds', 'w') as f:
        for segment in topics_segments:
            f.write(str(segment[0]) + ' ' + str(segment[1]) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sc_file', type=str, default=None, help='seconds file path')
    parser.add_argument('--topic_file', type=str, default=None, help='topic file path')

    args = parser.parse_args()
    sc_file = args.sc_file
    topic_file = args.topic_file
    main(topic_file, sc_file)
