#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 16:19:28 2018

@author: driebel
"""

import praw


def post_bot(post_link, image_link):

    with open('reddit_bot_configuration.dat') as f:
        bot_config = f.read()
        bot_config = bot_config.split('\n')
        
    client_id = bot_config[0]
    client_secret = bot_config[1]
    user_agent = bot_config[2]
    password = bot_config[3]
    username = bot_config[4]
    
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, 
                         user_agent=user_agent, password = password, username = username)
    
    subreddit = reddit.subreddit('DepthHubImages')
    image_link = r'http:\\\\www.goole.image.link'
    post_link = r'http:\\\\original.post.link'
    title = 'Bot test6'
    body_text = "Hi!  I'm a friendly bot!  There's a cool DepthHub post at {}. \
    I think a really good related image can be found here {}.  \
    Sorry if I'm a little bit racist!".format(post_link, image_link)
    
    _ = subreddit.submit(title = title,selftext = body_text)