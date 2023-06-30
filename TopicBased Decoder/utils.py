import re

# this fuction is used to read the topic file and return a list of topics
def read_topic_file(topic_file):
    topic_list = []
    # read the topic file and split it on the new line
    with open(topic_file, 'r') as f:
        topics = f.read().split('\n')
    # for each topic in the topics list
    for topic in topics:
        # if the topic is not empty
        if topic != '':
            # split the topic on the space
            words = re.split(r'\s', topic)
            print(words)
            # append the words of the topic to the topic list
            topic_list.append(words)
    # return the topic list
    return topic_list

# this function reads the seconds file and returns a list of words corresponding to its seoconds
def read_seconds_file(seconds_file):
    seconds_list = []
    # read the seconds file and split it on the new line
    with open(seconds_file, 'r') as f:
        seconds = f.read().split('\n')
    # for each second in the seconds 
    for second in seconds:
        # if the second is not empty
        if second != '':
            # match the second with the regex before the open bracket (
            words = re.match(r'(.*)\s\(', second)
            if(words):
              words = words.group(1)
              # split the words on the space
              words = re.split(r'\s', words)
              # append the words of the second to the seconds list
              seconds_list.append(words)

    # return the words list
    return seconds_list

# this function is used to compare the seconds list with the topics list 
# and return a the starting and ending time of the topic
def compare_seconds_with_topics(seconds_list, topic_list):
    # for each topic in the topic list
    topics_segments = []
    start_second = 0
    for topic in topic_list:
        for second in range(start_second, len(seconds_list)):
            # if all the words in the second are in the topic
            if not all(word in topic for word in seconds_list[second]):
                if start_second == second:
                    topics_segments.append((start_second, second + 1))
                    start_second = second + 1
                else:
                    topics_segments.append((start_second, second))
                    start_second = second + 1
                break
    topics_segments.append((start_second, len(seconds_list)))
    return topics_segments