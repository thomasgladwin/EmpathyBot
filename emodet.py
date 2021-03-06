print('Gathering psychic powers...')

import re
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
word_vectors = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True, limit=200000)
# word_vectors.save('wvsubset') 
# word_vectors = KeyedVectors.load("wvsubset", mmap='r')
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r"\w+")
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

read_WVM_from_file = False

def read_words():
    words = []
    fid = open('emotional_words2.txt', 'r') 
    while True:
        line = fid.readline()
        if not line: 
            break
        if len(line) > 0:
            word = tokenizer.tokenize(line)
            words.append(word[0])
    fid.close()
    return words

def get_WVM():
    words = read_words()
    words = [lemmatizer.lemmatize(word) for word in words]
    # Select adjectives (?)
    # words = [word0 for word0 in words if pos_tag([word0])[0][1] in ['JJ', 'JJR', 'JJS', 'NN', 'RB', 'RBR', 'RBS']]
    # Select words known by word_vectors
    emowords = [word0 for word0 in words if word0 in word_vectors.vocab]
    emowords = set(emowords)
    emowords = [word0 for word0 in emowords]
    WVM = np.array([word_vectors[word0] for word0 in emowords])
    return emowords, WVM

if read_WVM_from_file:
    emowords = np.load('emowords.npy')
    WVM = np.load('WVM.npy')
else:
    emowords, WVM = get_WVM()
    np.save('emowords', emowords)
    np.save('WVM', WVM)

def emodet(text_all):
    sentences = re.split(r'[,;.-]', text_all) 
    sims_all = []
    for text in sentences:
        if len(text) == 0:
            continue
        tokens = tokenizer.tokenize(text)
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        tokens = [token0 for token0 in tokens if token0 in word_vectors.vocab]
        # Test for negation-tokens (for adjectives)
        neg_v = [np.dot(word_vectors['not'] - word_vectors['very'], word_vectors[token]) for token in tokens]
        neg_v = np.array(neg_v)
        # For nouns
        #neg_v2 = [np.dot(word_vectors['lose'] - word_vectors['gain'], word_vectors[token]) for token in tokens]
        #neg_v = neg_v + np.array(neg_v2)
        nonnegation = 1 - 2 * np.mod(len(neg_v[neg_v > 1]), 2)
        # Get nouns and adjectives after preprocessing
        pt = pos_tag(tokens);
        tokens2 = [x[0] for x in pt if x[1] in ['JJ', 'NN', 'RB', 'VB']]
        if len(tokens2) > 0:
            tokens = tokens2
        # Find strongest match to an emotion
        token_sims = []
        for token0 in tokens:
            sims0 = [nonnegation * np.dot(word_vectors[token0], WVMv) for WVMv in WVM]
            token_sims.append(sims0)
        sims_all.append(token_sims)
    # Get emotional meaning per sentences and average the vector
    nEmos_per_token = 3
    nEmos_total = 3
    emo_indices = []
    emo_sims = []
    for sentence_level in sims_all:
        for token_level in sentence_level:
            token_level = np.array(token_level)
            indices = np.argsort(token_level)
            emo_indices.append(indices[-nEmos_per_token:])
            token_level_s = token_level[indices]
            emo_sims.append(token_level_s[-nEmos_per_token:])
    # mswv = word_vectors.most_similar(positive=[sims])
    emo_indices = np.array(emo_indices).flatten()
    emo_sims = np.array(emo_sims).flatten()
    # return sims_all, emo_indices, emo_sims
    indices = np.argsort(emo_sims)
    indices = emo_indices[indices]
    output = 'I sense you are feeling... '
    iEmo = 1
    nEmo = 0
    used_indices = []
    while nEmo < nEmos_total:
        this_index = indices[-iEmo]
        if not this_index in used_indices:
            output = output + emowords[this_index] + "... "
            used_indices.append(this_index)
            nEmo = nEmo + 1
        iEmo = iEmo + 1
    print(output)
    return output
