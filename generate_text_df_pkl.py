import praw
import re
import pickle as pkl

from reddit_user_info import main as rui_main

import pandas as pd


_reddit    = None
_subreddit = None
_initiated = False


# Start up the praw client
def _initiate_client():
    
    global _reddit
    global _subreddit
    global _initiated

    client_id, client_secret, user_agent = rui_main()
    
    _reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, 
                         user_agent=user_agent)

    _subreddit = _reddit.subreddit('DepthHub')
    _initiated = True
    
# Get the most recent post urls
def get_url( limit = 10 ):
    
    # Set up client if not already
    if ( not _initiated ):
        _initiate_client()
    
    original_post_urls = []
    # Pull the newest <limit> posts from DepthHub
    for submission in _subreddit.new(limit=limit):
        original_post_urls.append(submission.url)
    return original_post_urls

# Get the subreddit from each of the posts
def get_subreddit( original_post_urls ):

    # Set up client if not already
    if ( not _initiated ):
        _initiate_client()
    
    # Id dict uses the comment id as key, and contains subreddit
    pattern  = r'[/ ?]'
    id_dict  = {}
    
    for i in original_post_urls:

        try:
            tokens = re.split(pattern,i) # Break the url by slashes into elements
            
            # subreddits are of the form r/askscience, for example
            subreddit_index = tokens.index('r') + 1
            subreddit = tokens[ subreddit_index ]

            comment_ids = []
            comment_objects = _reddit.submission(url=i).comments.list()
            for j in comment_objects:
                comment_ids.append(j.id)

            counter = 0

            # Get the id
            for token in tokens:
                if token in comment_ids:
                    id_dict[token] = subreddit
                    
        except praw.exceptions.ClientException:
            pass
        
    return id_dict
    
    
# Extract the text of the post
def get_text( id_sub_dict ):
    
    # Set up client if not already
    if ( not _initiated ):
        _initiate_client()

    # Use keys from sub dict as comment ids to 
    #  use to locate text
    text_dict = {}
    for key in id_sub_dict.keys():
        comment = _reddit.comment( id=key )
        text_dict[ key ] = comment.body

    return text_dict

# Turn the text and subreddits in a data frame
def gen_df( sub_dict, text_dict ):
    out_df = pd.DataFrame( columns=['comment_id','subreddit','text'] )

    key_list = list( sub_dict.keys() )

    for i in range( 0, len(sub_dict.keys()) ): 
        s_key = key_list[i]
        out_df = out_df.append( 
            {
                'comment_id':s_key,
                'subreddit':sub_dict[s_key],
                'text':text_dict[s_key],
            }, ignore_index=True )
    return out_df
    
# Turn the dicts into a pd dataframe
#  pickle the dataframe
def write_df( filename, out_df ):
    
    with open( filename, 'wb' ) as f:
        pkl.dump( out_df, f )
    
    
# Gets only the most recent n_submission files
def get_recent( n_submissions=5 ):
    
    # Do all the stuff
    _initiate_client()
    urls = get_url( n_submissions )
    sub_dict = get_subreddit(urls)
    txt_dict = get_text( sub_dict )
    return gen_df( sub_dict, txt_dict )
    
    
# Get the top n_sub posts, check if in dataframe,
#  and update the file if there is anything new
def update_post_file( filename, n_submissions=5 ):
    
    # Read what is in the old file
    old_df = pd.read_pickle( filename )
    
    # Get the most recent posts to the subreddit
    recent_df = gtp.get_recent( n_submissions )
    
    # Determine if post ids are already present
    new_posts = recent_df['comment_id'].apply( 
        lambda x: x not in old_df['comment_id'].values 
    )
    
    # Get number of new posts, if none abort
    n_new = new_posts.sum()
    if ( n_new == 0 ):
        return

    # If new posts, add and write new file
    out_df = recent_df[ new_posts ].append( old_df, ignore_index=True )
    out_df.to_pickle( filename )
    
    
def main():
    
    # Read and groom the input
    output_file   = input("Enter filename: ")
    n_submissions = input("Number of posts to grab: ")
    
    n_submissions = int( n_submissions )
    
    if ( output_file[-4:] != '.pkl' ):
        output_file = output_file + '.pkl'
    
    # Do all the stuff
    print('Initiating client...')
    _initiate_client()
    urls = get_url( n_submissions )
    print('Exctracting data...')
    sub_dict = get_subreddit(urls)
    txt_dict = get_text( sub_dict )
    out_df   = gen_df( sub_dict, txt_dict )
    
    # Do the writing
    write_df( output_file, out_df )
    print('Wrote file: ' + output_file )
    
    
if __name__ == "__main__":
    main()