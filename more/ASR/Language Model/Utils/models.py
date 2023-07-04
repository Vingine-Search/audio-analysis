from nltk import bigrams, trigrams, FreqDist
import numpy as np


class UnigramLM:
        # The class constructor takes the vocabulary
        # creates a |V| numpy 1D array for the uni-gram model filled with zeros
        # It also creates two dictionaries to be used for token identification
        def __init__(self, vocab):
            self.id2word = {i: word for i, word in enumerate(list(vocab))}
            self.word2id = {word: i for i, word in self.id2word.items()}
            self.vocab_size = len(vocab)
            self.vocab = vocab
            # create a numpy |V| 1D array filled with zeros
            self.CountsArray = np.zeros(self.vocab_size, dtype=int)
        
        # This function is responsible for training the Language Model
        # It is given the preprocessed training set sentences
        # The goal is to fill the 1D array with the appropriate counts
        # hint: loop over the sentences to fill the array with the appropriate counts
        def train(self, train_sentences):
            for sentence in train_sentences:
                for word in sentence:
                    if word in self.vocab:
                        self.CountsArray[self.word2id[word]] += 1
        
        # this function takes a word and calculates the Add-one Smoothed uni-gram probability of it
        # Of course the function will make use of the 1D counts array built while training
        # The function must return the calculated probability
        def calcProbability(self, word):
            if word in self.vocab:
                return (self.CountsArray[self.word2id[word]] + 1) / (np.sum(self.CountsArray) + self.vocab_size)
            return 0
        
        def getSum_z1(self):
            z_1 = self.CountsArray > 0
            z1_index = np.where(z_1 == True)[0]
            z1_sum = sum([self.calcProbability(self.id2word[i]) for i in z1_index])
            return (1 - z1_sum)
##############################################################################################################

class BigramLM:
    
    # The class constructor takes the vocabulary
    # creates a |V| * |V| numpy 2D matrix for the bi-gram model filled with zeros
    # It also creates two dictionaries to be used for token identification
    def __init__(self, vocab):
        self.id2word = {i: word for i, word in enumerate(list(vocab))}
        self.word2id = {word: i for i, word in self.id2word.items()}
        self.vocab_size = len(vocab)
        self.vocab = vocab
        # create a numpy |V| * |V| 2D array filled with zeros
        self.CountsMatrix = np.zeros((self.vocab_size, self.vocab_size), dtype=int)
    
    # This function is responsible for training the Language Model
    # It is given the preprocessed training set sentences
    # The goal is to fill the 2D matrix with the appropriate counts
    # hint: check bigrams() and FreqDist() from nltk
    # hint: loop over the sentences to fill the matrix with the appropriate counts
    def train(self, train_sentences):
        for sentence in train_sentences:
            train_bigrams = bigrams(sentence)
            freqDests_pairs = FreqDist(train_bigrams)
            for k, v in freqDests_pairs.items():
                if k[0] in self.vocab and k[1] in self.vocab:
                    self.CountsMatrix[self.word2id[k[0]], self.word2id[k[1]]] += v                
                
    
    # this function takes two words and calculates the Add-one Smoothed bi-gram probability of it
    # Of course the function will make use of the 2D counts matrix built while training
    # The function assumes that word1 precedes word2
    # The function must return the calculated probability
    def calcProbability(self, word1, word2):
        if word1 in self.vocab and word2 in self.vocab:
            return (self.CountsMatrix[self.word2id[word1], self.word2id[word2]] + 1) / (np.sum(self.CountsMatrix[self.word2id[word1], :]) + self.vocab_size)
        return 0
    
    def getCounts(self):
        return self.CountsMatrix
    
    def checkBackOff(self, word1, word2):
        if word1 in self.vocab and word2 in self.vocab and self.CountsMatrix[self.word2id[word1], self.word2id[word2]] == 0:
            return True
        return False
    
    def getSum_z1(self, word):
        context_index = self.word2id[word]
        z_1 = self.CountsMatrix[context_index, :] > 0
        z1_index = np.where(z_1 == True)[0]
        z1_sum = sum([self.calcProbability(word, self.id2word[i]) for i in z1_index])
        return (1 - z1_sum)
##############################################################################################################

class TrigramLM:
    
    # The class constructor takes the vocabulary
    # creates a (|V| * |V|) * |V| numpy 2D matrix for the tri-gram model filled with zeros
    # It also creates two dictionaries to be used for token identification
    def __init__(self, vocab):
        context_list = [(c1, c2) for c1 in list(vocab) for c2 in list(vocab)]
        self.id2pair = {i: pair for i, pair in enumerate(context_list)}
        self.pair2id = {pair: i for i, pair in self.id2pair.items()}
        
        self.id2word = {i: word for i, word in enumerate(list(vocab))}
        self.word2id = {word: i for i, word in self.id2word.items()}

        self.vocab_size = len(vocab)
        self.vocab = vocab
    
        # create a numpy (|V| * |V|) * |V| 2D array filled with zeros
        self.CountsMatrix = np.zeros((self.vocab_size * self.vocab_size, self.vocab_size), dtype=int)
    

    # This function is responsible for training the Language Model
    # It is given the preprocessed training set sentences
    # The goal is to fill the 2D matrix with the appropriate counts
    # hint: loop over the sentences to fill the matrix with the appropriate counts
    def train(self, train_sentences):
        for sentence in train_sentences:
            train_trigrams = trigrams(sentence)
            freqDests_pairs = FreqDist(train_trigrams)
            for k, v in freqDests_pairs.items():
                if k[0] in self.vocab and k[1] in self.vocab and k[2] in self.vocab:
                    self.CountsMatrix[self.pair2id[(k[0], k[1])], self.word2id[k[2]]] += v     
                  
                
    
    # this function takes two words and calculates the Add-one Smoothed bi-gram probability of it
    # Of course the function will make use of the 2D counts matrix built while training
    # The function assumes that word1 precedes word2
    # The function must return the calculated probability
    def calcProbability(self, word1, word2, word3):
        if word1 in self.vocab and word2 in self.vocab and word3 in self.vocab:
            return (self.CountsMatrix[self.pair2id[(word1, word2)], self.word2id[word3]] + 1) / (np.sum(self.CountsMatrix[self.pair2id[(word1, word2)], :]) + self.vocab_size)
        return 0
        

    def checkBackOff(self, word1, word2, word3):
        if word1 in self.vocab and word2 in self.vocab and word3 in self.vocab and self.CountsMatrix[self.pair2id[(word1, word2)], self.word2id[word3]] == 0:
            return True
        return False

    def getSum_z1(self, word1, word2):
        context_index = self.pair2id[(word1, word2)]
        z_1 = self.CountsMatrix[context_index, :] > 0
        z1_index = np.where(z_1 == True)[0]
        z1_sum = sum([self.calcProbability(word1, word2, self.id2word[i]) for i in z1_index])
        return (1 - z1_sum)
##############################################################################################################
    