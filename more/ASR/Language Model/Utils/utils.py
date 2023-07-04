import numpy as np
from nltk.tokenize import word_tokenize
import pickle

# load data from data directory
def loadData(dataDir):
    with open(dataDir,'r') as f:
        train = [l.strip() for l in f.readlines()]
    return train

# This function takes a List of sentences to preprocess them and vocabulary to extend
# It returns a list of sentences after preprocessing and the vocabulary it found
def preprocess(sentences):
    tokenized_sentences = []
    for i in range(len(sentences)):
        sentence = sentences[i]

        # convert all characters to lower (hint: use lower())
        sentence =  sentence.lower()
        
        # tokenize the sentence (hint: use word_tokenize())
        tokenized_senetence = word_tokenize(sentence)
        
        # Add the start sentence <s> and end sentence </s> tokens at the beginning and end of each tokenized sentence
        tokenized_senetence.insert(0, "<s>")
        tokenized_senetence.insert(len(tokenized_senetence), "</s>")
        
        # Add the tokens of the sentence in the predefined set vocab to collect the vocabulary
        #for element in tokenized_senetence:
        #    vocab.add(element)
        
        # Add the sentence to the tokenized_sentences
        tokenized_sentences.append(tokenized_senetence) 
    
    return tokenized_sentences

# load the vocabulary from the file
# The function takes the path to the vocabulary file
# The function returns the vocabulary
def loadVocab(vocabDir):
    with open(vocabDir,'r') as f:
        vocab=[l.split()[0] for l in f.readlines()]
    return vocab


# Calculate backoff weights in case of unseen context for a given sentence
# The function takes a sentence and the two language models (trigram anf bigram)
# The function returns the probability of the sentence
def calcProbability(sentence, bigramLM, trigramLM, unigramLM):
    word1, word2 = sentence[0], sentence[1]
    target = sentence[2]
    bo_weight = 1
    if trigramLM.checkBackOff(word1, word2, target):
        bo_weight = trigramLM.getSum_z1(word1, word2) / bigramLM.getSum_z1(word2)
        if bigramLM.checkBackOff(word2, target):
            return bo_weight * (bigramLM.getSum_z1(word2) / unigramLM.getSum_z1()) * unigramLM.calcProbability(target)
        return bo_weight * bigramLM.calcProbability(word2, target)
    else:
        return trigramLM.calcProbability(word1, word2, target)


# This function is (not correctly) implemented
# Calculate backoff weights in case of unseen context for a given sentence
def backOffWeight_uni_context(word, bigramLM, unigramLM):
    return (bigramLM.getSum_z1(word) / unigramLM.getSum_z1())


# This function is (correctly) implemented
# Calculate backoff weights in case of unseen context for a given sentence
# The function takes a sentence and the two language models (trigram anf bigram)
def backOffWeight_bi_context(sentence, bigramLM, trigramLM):
    word1, word2 = sentence[0], sentence[1]
    return trigramLM.getSum_z1(word1, word2) / bigramLM.getSum_z1(word2)

#save the model using pickle
def saveModel(model, filename):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)

#load the model using pickle
def loadModel(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model
