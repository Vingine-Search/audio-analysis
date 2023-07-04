import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from .whisper_asr.asr import main as asr
from .topic_segmentation.predict_mod import predict
from .whisper_asr.bounder import main as bound


def main(video_file):
    base_file = os.path.splitext(video_file)[0]
    audio_file = video_file # asr() can deal with .mp4 files just fine
    #base_file, audio_file = convert_to_mp3(video_file)
    # Generates base_file.txt, base_file.vtt, base_file.asr
    asr(audio_file)
    # Generates base_file.topics
    predict(base_file + ".txt")
    # Generates base_file.bounds
    bound(base_file + ".topics", base_file + ".asr")
    # We don't need the text file after splitting it
    os.remove(base_file + ".txt")


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
