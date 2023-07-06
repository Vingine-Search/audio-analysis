import os
import string
import whisperx
import argparse


# 1. Transcribe with original whisper (batched)
model = None

# 2. Align whisper output
model_a, metadata = None, None


def norm_word(word: str):
    for p in string.punctuation:
        word = word.replace(p, '')
    return word.replace(' ', '').lower()


def main(audio_file):
    global model, model_a, metadata
    if model == None:
        model = whisperx.load_model("base.en", "cuda", compute_type="float16")
        model_a, metadata = whisperx.load_align_model(language_code="en", device="cuda")

    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=1, language="en")

    result = whisperx.align(result["segments"], model_a, metadata, audio, "cuda", return_char_alignments=False)

    # Some words don't have a 'start', like numbers.
    lines = [(line['text'], line['start'], line['end']) for line in result['segments'] if 'start' in line]
    words = [(norm_word(word['word']), word['start'], word['end']) for word in result['word_segments'] if 'start' in word]

    noext, _ = os.path.splitext(audio_file)

    # write the transcript to a file
    with open(noext + '.txt', 'w') as f:
        ws = [word[0] for word in words]
        f.write(' '.join(ws))

    # write the transcript as vtt file
    with open(noext + '.vtt', 'w') as f:
        f.write('WEBVTT\n\n')
        for text, start, end in lines:
            f.write('{} --> {}\n'.format(start, end))
            f.write(text.strip() + '\n\n')

    # write the words per second to a file
    with open(noext + '.asr', 'w') as f:
        second, word_buffer = 1, []
        for word, start, _ in words:
            while start > second:
                f.write(' '.join(word_buffer) + '\n')
                second, word_buffer = second + 1, []
            word_buffer.append(word)
        f.write(' '.join(word_buffer) + '\n')


if __name__ == '__main__':
    # first read the audio file and its extension
    parser = argparse.ArgumentParser(description='Transcribe an audio file to text.')
    parser.add_argument('--audio', type=str, required=True, help='The audio file to transcribe.')
    args = parser.parse_args()

    main(args.audio)