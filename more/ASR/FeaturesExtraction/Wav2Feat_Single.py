import os
import soundfile as sf
import numpy as np
import htk_featio as htk
import speech_sigproc as sp
import argparse

# read wav file from user using Argparse
parser = argparse.ArgumentParser(description='Wav2Feat')
parser.add_argument('--wav_file', type=str, default=None, help='path to wav file')
parser.add_argument('--feat_file', type=str, default=None, help='feature file name')

args = parser.parse_args()
wav_file = args.wav_file
feat_file = args.feat_file


if not os.path.isfile(wav_file):
    raise RuntimeError('input wav file is missing. Have you downloaded the LibriSpeech corpus?')

samp_rate = 16000

x, s = sf.read(wav_file)
if (s != samp_rate):
    raise RuntimeError("LibriSpeech files are 16000 Hz, found {0}".format(s))

fe = sp.FrontEnd(samp_rate=samp_rate,mean_norm_feat=True)


feat = fe.process_utterance(x)

htk.write_htk_user_feat(feat, feat_file)
print("Wrote {0} frames to {1}".format(feat.shape[1], feat_file))




