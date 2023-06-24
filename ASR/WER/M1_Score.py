import argparse
import wer
import re

# create a function that calls wer.string_edit_distance() on every utterance
# and accumulates the errors for the corpus. Then, report the word error rate (WER)
# and the sentence error rate (SER). The WER should include the the total errors as well as the
# separately reporting the percentage of insertions, deletions and substitutions.
# The function signature is
# num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=reference_string, hyp=hypothesis_string)
#

def read_files(ref, hyp):
    ref_str = open(ref, "r").read()
    hyp_str = open(hyp, "r").read()
    return ref_str, hyp_str

def clean_from_ids(sentences):
    sentences_map = {}
    for sentence in sentences:
        id = re.search(r"(?<=\().*(?=\))", sentence)
        tokenized_sentence = re.split(r"\s", re.sub(r"\s*\(.*\)", "", sentence))
        sentences_map[id.group()] = tokenized_sentence
    return sentences_map

def score(ref_trn=None, hyp_trn=None):
    ref_str, hyp_str = read_files(ref_trn, hyp_trn)

    ref_sentences = re.split(r"\n", ref_str)
    hyp_sentences = re.split(r"\n", hyp_str)
    ref_sentences.pop(len(ref_sentences) - 1)
    hyp_sentences.pop(len(hyp_sentences) - 1)

    ref_map = clean_from_ids(ref_sentences)
    hyp_map = clean_from_ids(hyp_sentences)

    total_del, total_ins, total_sub, total_tokens, total_err = 0, 0, 0, 0, 0
    wrong_senetences = 0
    outputs = []
    for key in ref_map.keys():
        tokens, edits, deletions, insertions, substitutions = wer.string_edit_distance(ref_map[key], hyp_map[key])
        total_tokens += tokens
        total_err += edits
        total_ins += insertions
        total_del += deletions
        total_sub += substitutions
        wrong_senetences = wrong_senetences + 1 if edits > 0 else wrong_senetences
        output = "id: ({})\nScores: N={}, S={}, D={}, I={}\n\n".format(key, tokens, substitutions, deletions, insertions)
        outputs.append(output)
    
    ser = "---------------------------------\nSentence Error Rate:\nSum:N={}, Err={}\nAvg: N={}, Err={}%\n".format(len(ref_sentences), wrong_senetences, len(ref_sentences), wrong_senetences * 100/len(ref_sentences))
    wer_result ="""---------------------------------\nWord Error Rate:\nSum: N={}, Err={}, Sub={}, Del={}, Ins={}\nAvg: N={}, Err={}%, Sub={}%, Del={}%, Ins={}%\n-----------------------------------""".format(total_tokens, total_err, total_sub, total_del, total_ins, total_tokens, total_err *100/total_tokens, total_sub*100/total_tokens, total_del*100/total_tokens, total_ins*100/total_tokens)
    # write outputs, ser and wer_result to file named "score.txt"
    with open("score.txt", "w") as f:
        for output in outputs:
            f.write(output)
        f.write(ser)
        f.write(wer_result)
 
    return


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Evaluate ASR results.\n"
                                                 "Computes Word Error Rate and Sentence Error Rate")
    parser.add_argument('-ht', '--hyptrn', help='Hypothesized transcripts in TRN format', required=True, default=None)
    parser.add_argument('-rt', '--reftrn', help='Reference transcripts in TRN format', required=True, default=None)
    args = parser.parse_args()

    if args.reftrn is None or args.hyptrn is None:
        RuntimeError("Must specify reference trn and hypothesis trn files.")

    score(ref_trn=args.reftrn, hyp_trn=args.hyptrn)
