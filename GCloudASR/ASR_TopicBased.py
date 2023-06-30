import subprocess
import argparse

# first read the audio file and its extension
parser = argparse.ArgumentParser(description='Transcribe an audio file to text.')
parser.add_argument('--audio', type=str, required=True, help='The audio file to transcribe.')
parser.add_argument('--ext', type=str, required=True, help='The extension of the audio file.')
args = parser.parse_args()


file_name = args.audio.split('.')[0]

# files needed for the topic segemnter by text and by seconds
seconds_file = file_name + '.seconds'
transcript_file = file_name + '.txt'

# calling asr.py
subprocess.run(['python3', 'asr.py', '--audio', args.audio, '--ext', args.ext])

# ------ ADD YOUR CODE HERE FOR TOPIC SEGMENTATION BY TEXT ------

# ----------------------------------------------------------------

# don't forget to change the topic_file variable
topic_file = ""

# calling ASR_TopicSegemnatation.py
subprocess.run(['python3', 'ASR_TopicSegemnatation.py', '--sc_file', seconds_file, '--topic_file', topic_file])
