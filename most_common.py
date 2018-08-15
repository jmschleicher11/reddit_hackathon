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
reddit_df = pd.read_pickle(reddit_file)


def most_common(df, N=5):
    """
    Simple preprocessing pipeline which uses RegExp, sets basic token requirements,
    and removes default stop words.
    """
    print('preprocessing article text...')

    # tokenizer, stops, and stemmer
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = stopwords.words('english')  # can add more stop words to this set
    stop_words.append('would')
    lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer('english')
    df['top_n_lemma'] = ''
    df['top_n_stem'] = ''

    # process articles

    for row, post in enumerate(df['text']):
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
        # Extract top N words
        lemma_vectorizer = CountVectorizer()
        lemmed_article = ' '.join(wd for wd in lemmatized_tokens)
        article_lemma_vect = lemma_vectorizer.fit_transform([lemmed_article])
        lemma_freqs = [(word, article_lemma_vect.getcol(idx).sum()) 
                        for word, idx in lemma_vectorizer.vocabulary_.items()]
        top5_lemma = sorted(lemma_freqs, key = lambda x: -x[1])[0:N]
        df['top_n_lemma'].iloc[row] = [i[0] for i in top5_lemma]
        
        stem_vectorizer = CountVectorizer()
        lemmed_article = ' '.join(wd for wd in lemmatized_tokens)
        stemmed_article = ' '.join(wd for wd in stemmed_tokens)
        # performe a count-based vectorization of the document
        article_lemma_vect = lemma_vectorizer.fit_transform([lemmed_article])
        article_stem_vect = stem_vectorizer.fit_transform([stemmed_article])
        lemma_freqs = [(word, article_lemma_vect.getcol(idx).sum()) 
                        for word, idx in lemma_vectorizer.vocabulary_.items()]
        stem_freqs = [(word, article_stem_vect.getcol(idx).sum())
                        for word, idx in stem_vectorizer.vocabulary_.items()]
        

        top5_stem = sorted(stem_freqs, key = lambda x: -x[1])[0:N]
        df['top_n_stem'].iloc[row] = [i[0] for i in top5_stem]
        df['stem_counts'].iloc[row] = [i[0] for i in top5_stem]
                    
        return df
        


