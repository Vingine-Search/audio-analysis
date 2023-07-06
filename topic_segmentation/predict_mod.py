import os
import shutil
import logging
import tempfile
import numpy as np

from . import utils
from . import config
from . import preprocess
from . import recordgen
from .TLT import *

config.epochs = 1
config.batch_size = 1
config.snippet_stride = 1

dir_name = os.path.dirname(__file__)
vocab = utils.load_wordvecs(os.path.join(dir_name, config.word2vec_file_path))
logging.info("Loaded the vocab for TLT")
weights = utils.load_model_weights(os.path.join(dir_name, config.model_store))
logging.info("Loaded TLT model weights")
model = None

def init_topic():
    global model
    model = TwoLevelTransformerModel(weights)

def predict(input_file):
    global model
    if model == None:
        init_topic()

    output_file = os.path.splitext(input_file)[0] + ".topics"
    input_dir = tempfile.mkdtemp()
    original_input_file, input_file = input_file, os.path.join(input_dir, os.path.basename(input_file))
    shutil.copyfile(original_input_file, input_file)

    clean_asr, recovery_list = preprocess.recoverable_clean_section(open(input_file).read().strip(), vocab)

    tfrecord_tmpl = os.path.join(input_dir, config.tfrecord_tmpl)
    recordgen.record_gen_predict(clean_asr, tfrecord_tmpl, vocab)

    snippet_estimations = model.predict(recordgen.get_dataset(tfrecord_tmpl, True))
    snippet_estimations = np.reshape(snippet_estimations, (-1, config.snippet_length))

    clean_asr = clean_asr.split()
    segmented_clean_asr = [clean_asr[x:x + config.segment_length] for x in range(0, len(clean_asr), config.segment_length)]
    # Remove the last segment if it wasn't a full `config.segment_length`.
    if len(segmented_clean_asr[-1]) != config.segment_length:
        segmented_clean_asr.pop()
    snipped_clean_asr = [segmented_clean_asr[x:x + config.snippet_length] for x in range(0, len(segmented_clean_asr), config.snippet_stride)]
    # Remove the snippets which aren't a full `config.snippet_length`. Note that there are many and not only one since snippet_stride == 1.
    for i, snippet in enumerate(snipped_clean_asr):
        if len(snippet) != config.snippet_length:
            snipped_clean_asr = snipped_clean_asr[:i]
            break

    # Calculate the boundaries.
    boundaries = [[] for _ in range(len(segmented_clean_asr))]
    for snippet_index, segment_estimations in enumerate(snippet_estimations):
        for segment_index, segment_estimation in enumerate(segment_estimations):
            real_segment_index = snippet_index + segment_index
            boundaries[real_segment_index].append(segment_estimation)

    # Recover the original text and inject the boundary markers.
    words = []
    original_asr_index = 0
    for segment, b in zip(segmented_clean_asr, boundaries):
        # If this segment is a boundary, prepend two line breaks before writing it.
        if original_asr_index != 0 and config.is_boundary(b):
            words.append("\n\n")

        # Write the segment and sync it with the original word list.
        for word in segment:
            while word != utils.make_ascii(recovery_list[original_asr_index]):
                words.append(recovery_list[original_asr_index])
                original_asr_index += 1
            words.append(recovery_list[original_asr_index])
            original_asr_index += 1

    # Write the rest of the words that didn't make a full segment.
    for word in recovery_list[original_asr_index:]:
        words.append(word)

    open(output_file, 'w').write(' '.join(words).replace(" \n\n ", "\n\n"))
    shutil.rmtree(input_dir)
