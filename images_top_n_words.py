#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 20:16:22 2018

@author: Floreana
"""

import pandas as pd
from google_images_download import google_images_download
import os

pickle_loc = '10word_df.pkl'
reddit_df = pd.read_pickle(pickle_loc)

# scrape images of each from google images
n_images = 1
response = google_images_download.googleimagesdownload()
for row, words in enumerate(reddit_df['top_n_lemma']):
    print('proccesing {} of {}'.format(row, reddit_df.shape[0]))
    arguments={'keywords':" ".join(words), 
               'limit':n_images, 
               'format':'jpg',
               'prefix':str(row) + " ".join(words),
               'image_directory':os.path.join('lemma_images'), 
               '--safe_search':''}
    absolute_image_paths = response.download(arguments)
    
for row, words in enumerate(reddit_df['top_n_stem']):
    print('proccesing {} of {}'.format(row, reddit_df.shape[0]))
    arguments={'keywords':" ".join(words), 
               'limit':n_images, 
               'format':'jpg',
               'prefix':str(row) + " ".join(words),
               'image_directory':os.path.join('stem_images'), 
               '--safe_search':''}
    absolute_image_paths = response.download(arguments)
    
