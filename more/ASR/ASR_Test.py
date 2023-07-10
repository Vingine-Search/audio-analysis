import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wav_file', type=str, default=None, help='wav file path')

    args = parser.parse_args()
    wav_file = args.wav_file 

    # extract wav file name when the path is given as ../samples/file_name.wav
    file_name = wav_file.split('/')[-1].split('.')[0]
    feat_file = file_name + '.feat'

    # extract features and save to feat_file
    subprocess.run(['python', 'FeaturesExtraction/Wav2Feat_Single.py', '--wav_file', wav_file, '--feat_file', feat_file])

    # decode the feature file and save to file_name.txt
    subprocess.run(['python', 'Decoder/StaticDecoder.py', '--feat', feat_file, '--am', 'Decoder/DNN_AM', '--decoding_graph', 'Decoder/DecodingGraph-large.fst.txt', '--label_map', 'Decoder/labels.ciphones', '--trn', file_name + '.txt'])


if __name__ == '__main__':
    main()