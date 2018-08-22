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

print('Initiating client...')
gtd._initiate_client()

for submission in gtd._subreddit.stream.submissions():

    print('New post! Extracting url and subreddit...')
    # Get url and subreddit info
    url_list = [ submission.url ]
    sub_dict, url_dict = gtd.get_subreddit( url_list )
    
    # Get the comment id, to see if already in list
    try:
        comment_id = list(sub_dict.keys())[0]
    except IndexError:
        comment_id = None
    if ( (comment_id not in old_ids) and
         (sub_dict != None) ):
        
        print('Unknown comment id %s, continuing...'%comment_id)
        
        # Continue to processing
        txt_dict = gtd.get_text( sub_dict )
        
        print('Extracting text...')
        
        # Generate the df with all the info
        out_df = gtd.gen_df( sub_dict, txt_dict, url_dict )

        # If the text is present, can move on to analysis
        if ( not out_df.empty ):
            if ( len( out_df['text'].values[0] ) > 30 ):
            
                print('Read text, processing:')

                #######################
                ######Do stuff here####
                #######################


                # Do the processing and get the lemmatized words
                lemma_w, stem_w, lemma_n, stem_n = mc.most_common( out_df['text'].values[0] )

                print('Locating image...')
                # Get the image link using gogle images download
                image_link = itw.get_image_link( lemma_w )

                if ( image_link != None ):
                
                    print('Image found, posting...')

                    # Run the post bot
                    pb.post_bot(
                                post_link=out_df['url'].values[0], 
                                image_link=image_link, 
                                title=submission.title,
                                words=lemma_w,
                               )

                    print('Post complete! Updating database...')
                    #######################
                    #######################
                    #######################

                    # Add to dataframe pkl
                    gtd.update_post_pickle_with_df( out_df, filename=file_name )

                    print('Done!\n\n')
                    time.sleep(59)
                    
                # Image download error, image_link == None
                else:
                    print('Error downloading image, aborting\n\n')
                    
            # Short text in post, most likely "[deleted]"
            else:
                print('No text found, aborting\n\n')
                
        # Dataframe empty, found no text
        else:
            print('No text found, aborting\n\n')
            
    # Already posted for this image
    else:
        print('Comment id %s already present, ignoring\n\n'%comment_id)
    time.sleep(1)
