#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 14:03:24 2018

@author: driebel
"""

from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer

#file_dir = '/home/driebel/Dropbox/Insight/hackathon/reddit_hackathon/'
reddit_file = 'sample_comments_df_1000.pkl'
#reddit_df = pd.read_pickle(file_dir+reddit_file)
df = pd.read_pickle(reddit_file)
df = df[df['text'] != '[removed]']
df = df[df['text'] != '[deleted]']

def most_common(post, N=5):
    """
    Simple preprocessing pipeline which uses RegExp, sets basic token requirements,
    and removes default stop words.
    """
    print('preprocessing article text...')

    # tokenizer, stops, and stemmer
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = stopwords.words('english')  # can add more stop words to this set
    new_stops = ['org', 'wikipedia', 'en', 'wiki','would','http','https','youtube',
                 'www','com','de','al','___','askhistorians','askhistorian',
                 'km','__','use','lb']
    for word in new_stops:
        stop_words.append(word)
            
    lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer('english')
    #df['top_n_lemma'] = ''
    #df['top_n_stem'] = ''
    #df['lemma_counts'] = ''
    #df['stem_counts'] = ''
    # process articles

    stemmed_tokens = []
    lemmatized_tokens = []
    tokens = tokenizer.tokenize(post.lower())
    for token in tokens:
        if token not in stop_words:
            if len(token) > 0 and len(token) < 20: # removes non words
                if not token[0].isdigit() and not token[-1].isdigit(): # removes numbers
                    lemmatized_tokens.append(lemmatizer.lemmatize(token))
                    stemmed_tokens.append(stemmer.stem(token))
                    #cleaned_tokens.append(lemmatized_tokens)
    
    # Extract top N words Using Lemma
    lemma_vectorizer = CountVectorizer()
    lemmed_article = ' '.join(wd for wd in lemmatized_tokens)
    article_lemma_vect = lemma_vectorizer.fit_transform([lemmed_article])
    lemma_freqs = [(word, article_lemma_vect.getcol(idx).sum()) 
                    for word, idx in lemma_vectorizer.vocabulary_.items()]
    top5_lemma = sorted(lemma_freqs, key = lambda x: -x[1])[0:N]
    top_n_lemma = [i[0] for i in top5_lemma]
    lemma_counts = [i[1] for i in top5_lemma]
    
    # Using Stem
    stem_vectorizer = CountVectorizer()
    stemmed_article = ' '.join(wd for wd in stemmed_tokens)
    # performe a count-based vectorization of the document
    article_stem_vect = stem_vectorizer.fit_transform([stemmed_article])
    stem_freqs = [(word, article_stem_vect.getcol(idx).sum())
                    for word, idx in stem_vectorizer.vocabulary_.items()]
    top5_stem = sorted(stem_freqs, key = lambda x: -x[1])[0:N]
    top_n_stem = [i[0] for i in top5_stem]
    stem_counts = [i[1] for i in top5_stem]
 
    return top_n_lemma, top_n_stem, lemma_counts, stem_counts




                   
df.to_pickle('10word_df.pkl')
        
'''
Optional to output the key words to a text file for examination   

with open('key_words.txt','w') as f:
    for row in range(df.shape[0]):
        for i in df['top_n_lemma'].iloc[row]:
            f.write(i+' ')
        f.write('\n')
'''