from google.cloud import speech
from google.cloud import storage
import argparse

storage_client = storage.Client.from_service_account_json('key.json')
bucket_name = 'demo_audio_bucket_00'

def upload_to_bucket(blob_name, file_path, bucket_name):
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)
    return blob


# first read the audio file and its extension
parser = argparse.ArgumentParser(description='Transcribe an audio file to text.')
parser.add_argument('--audio', type=str, required=True, help='The audio file to transcribe.')
parser.add_argument('--ext', type=str, required=True, help='The extension of the audio file.')
args = parser.parse_args()

upload_to_bucket(args.audio, args.audio, bucket_name)

file_uri = 'gs://' + bucket_name + '/' + args.audio

# load the audio
file_name = args.audio
extension = args.ext
file = file_name.split('.')[0]
# initialize the client
client = speech.SpeechClient.from_service_account_file('key.json')

# # load the audio
# with open(file_name, 'rb') as audio_file:
#     content = audio_file.read()

# configure the audio settings
audio = speech.RecognitionAudio(uri=file_uri)

# configure the speech settings based on the extension of the audio file
# and enable word time offsets
if extension == 'wav':
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US',
        enable_word_time_offsets=True)
elif extension == 'flac':
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True)
elif extension == 'mp3':
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED, 
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True)

# transcribe the audio
operation = client.long_running_recognize(config=config, audio=audio)
response = operation.result()

# extract the text from the response
all_transcript = []
for result in response.results:
    all_transcript.append(result.alternatives[0].transcript)

all_transcript = ' '.join(all_transcript)



total_seconds = response.results[-1].alternatives[0].words[-1].end_time.seconds
# extract all the words per second
# Iterate over the words in the response
seconds = [[] for _ in range(total_seconds + 1)]
for result in response.results:
    for word in result.alternatives[0].words:
        start_time = word.start_time
        end_time = word.end_time
        word_text = word.word
        second = 0 if start_time.seconds == None else start_time.seconds
        seconds[second].append(word_text)



# write the transcript to a file
with open(file + '.txt', 'w') as f:
    f.write(all_transcript)

# write the transcript as vtt file
with open(file + '.vtt', 'w') as f:
    f.write('WEBVTT\n\n')
    for idx, second in enumerate(seconds):
        f.write('{}.00 --> {}.00\n'.format(idx, idx + 1))
        f.write(' '.join(second) + '\n\n')


# write the words per second to a file
with open(file + '.seconds', 'w') as f:
    for idx, second in enumerate(seconds):
        f.write(' '.join(second) + ' ({})'.format(idx) + '\n')

    