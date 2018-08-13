#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import praw
import re


#direct = '/Users/Floreana/Documents/Jobs/Insight/hackathon/'
#sys.path.append(direct) 

from reddit_user_info import main

client_id, client_secret, user_agent = main()
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, 
                     user_agent=user_agent)

subreddit = reddit.subreddit('DepthHub')

original_post_urls = []
# Pull the newest 20 posts from DepthHub
for submission in subreddit.new(limit=20):
    original_post_urls.append(submission.url)

pattern = r'[/ ?]'
found = []
for i in original_post_urls:
    #print("URL: ", depthhub_submission.url)
    tokens = re.split(pattern,i)
    comment_ids = []
    comment_objects = reddit.submission(url=i).comments.list()
    for j in comment_objects:
        comment_ids.append(j.id)
    for token in tokens:
        if token in comment_ids:
            found.append(token)

texts = []
# Access the body of the text from the good comments
for text in found:
    comment = reddit.comment(id=text)
    texts.append(comment.body)


## #### Playing with individual comments
#for submission in subreddit.hot(limit=5):
#    print("Title: ", submission.title)
#    print("URL: ", submission.url)
#    print("Score: ", submission.score)
#    print("---------------------------------\n")
#
#
##reddit.submission(url=test).selftext
#test = 'https://www.reddit.com/r/AskHistorians/comments/95d6b2/how_many_people_were_really_being_sacrificed/e3w87bi/?utm_content=permalink&utm_medium=front&utm_source=reddit&utm_name=AskHistorians'
#
#
#comment = reddit.submission(url=test)
#comment.comments.list()[0].id
#
#comment = reddit.comment(id='e3w87bi')
#comment.body

