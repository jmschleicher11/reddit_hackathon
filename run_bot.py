import datetime
import time

import pandas as pd

import generate_text_df_pkl as gtd
import most_common as mc
import images_top_n_words as itw
import post_bot as pb

# Want to stream, as items created,
#  add to file containing ids

file_name = 'post_data.pkl'

# Get which ids already exist
old_ids = list( pd.read_pickle( file_name )['comment_id'].values )

gtd._initiate_client()

counter = 0
for submission in gtd._subreddit.stream.submissions():

    # Get url and subreddit info
    url_list = [ submission.url ]
    sub_dict, url_dict = gtd.get_subreddit( url_list )
    
    # Get the comment id, to see if already in list
    comment_id = list(sub_dict.keys())[0]
    if ( comment_id not in old_ids ):
        
        # Continue to processing
        txt_dict = gtd.get_text( sub_dict )
        
        # Generate the df with all the info
        out_df = gtd.gen_df( sub_dict, txt_dict, url_dict )

        # If the text is present, can move on to analysis
        if ( not out_df.empty ):
            
            #######################
            ######Do stuff here####
            #######################
            
            # Do the processing and get the lemmatized words
            lemma_w, stem_w, lemma_n, stem_n = mc.most_common( out_df['text'].values[0] )
            
            # Get the image link using gogle images download
            image_link = itw.get_image_link( lemma_w )
            
            # Run the post bot
            pb.post_bot(
                        post_link=out_df['url'].values[0], 
                        image_link=image_link, 
                        title=submission.title,
                       )
            
            #######################
            #######################
            #######################
            
##################################################CHANGE THE FILE NAME
            # Add to dataframe pkl
            gtd.update_post_pickle_with_df( out_df, filename='placeholder.pkl' )
            
    time.sleep(0.5)
    
##############################################REMOVE COUNTER WHEN DONE TESTING
    if ( counter > 1 ):
        break
    counter += 1