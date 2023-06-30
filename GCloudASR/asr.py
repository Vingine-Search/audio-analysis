from google.cloud import speech
import argparse


# first read the audio file and its extension
parser = argparse.ArgumentParser(description='Transcribe an audio file to text.')
parser.add_argument('--audio', type=str, required=True, help='The audio file to transcribe.')
parser.add_argument('--ext', type=str, required=True, help='The extension of the audio file.')
args = parser.parse_args()

# load the audio
file_name = args.audio
extension = args.ext

# initialize the client
client = speech.SpeechClient.from_service_account_file('key.json')

# load the audio
with open(file_name, 'rb') as audio_file:
    content = audio_file.read()

# configure the audio settings
audio = speech.RecognitionAudio(content=content)

# configure the speech settings based on the extension of the audio file
if extension == 'wav':
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                    sample_rate_hertz=44100, language_code='en-US', enable_automatic_punctuation=True)
elif extension == 'flac':
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
                                    sample_rate_hertz=16000, language_code='en-US', enable_automatic_punctuation=True)
elif extension == 'mp3':
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                                    sample_rate_hertz=44100, language_code='en-US', enable_automatic_punctuation=True)

# transcribe the audio
response = client.recognize(config=config, audio=audio)

# extract the text from the response
print(response.results[0].alternatives[0].transcript)