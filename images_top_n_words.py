#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 20:16:22 2018

@author: Floreana
"""

import pandas as pd
from google_images_download import google_images_download
import os

def main():
    pickle_loc = '/Users/Floreana/Desktop/new_df.pkl'
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
                   'image_directory':os.path.join('images'), 
                   'safe_search':True, 
                   'print_urls':True}
        absolute_image_paths = response.download(arguments)

# Google the stem/lemma words, return
#  first image link as a string
def get_image_link( words, n_images=1,  ):
    
    # Set up directories we are working in
    work_dir = os.getcwd()    
    img_dir  = work_dir + '/downloads/images/'
    log_dir  = work_dir + '/logs/'
    
    kw_str = " ".join(words)
    
    print(kw_str)
    
    # Get the image and metadata
    response = google_images_download.googleimagesdownload()
    arguments={'keywords':kw_str, 
                   'limit':n_images, 
                   'format':'jpg',
                   'image_directory':os.path.join('images'), 
                   'safe_search':True, 
                   'extract_metadata':True,
                   'no_numbering':True,
                   'print_urls':True}
    absolute_image_paths = response.download(arguments)
    
    # Attempt to locate the image. If none, than return
    #  failstate, and we will ignore this image
    try:
        print( list(absolute_image_paths.values())[0][0] )
        downloaded_file = list(absolute_image_paths.values())[0][0]
    except IndexError:
        return None
    
    # Remove the image we downloaded, since we don't need it
    try:
        os.remove( downloaded_file )
    except FileNotFoundError:
        pass
    
    # The link to the image
    img_path = ''

    # Get data from log file
    # start by opening the log file
    with open( log_dir + kw_str + '.txt' , 'r' ) as f:
        # Parse line by line, looking for "image_link"
        for line in f:
            line_arr = line.split(" ")
            if ( '"image_link":' in line_arr ):
                use_line = line
                
        line_arr = use_line.split(" ")
        # File path is after image link
        index = line_arr.index('"image_link":')

        # Could in principle have link split across
        #  indexes, so combine everything from here to end
        for i in range( index+1, len(line_arr) ):
            img_path += line_arr[i]

        # Remove the quotes and \n character
        img_path = img_path[1:-3]
    print( img_path )
    
    try:
        os.remove( log_dir+kw_str+'.txt' )
    except FileNotFoundError:
        pass
        
    return img_path


if __name__ == '__main__':
    main()