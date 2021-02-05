import praw
import configparser
import time
import datetime
from praw.models import MoreComments

cp = configparser.RawConfigParser()   
configFilePath = './client.config'
cp.read(configFilePath)

current_client_id = cp.get('client-config', 'client_id')
current_client_secret = cp.get('client-config', 'client_secret')

reddit = praw.Reddit(
    user_agent="Comment Extraction (by u/chriskok1337)",
    client_id=current_client_id,
    client_secret=current_client_secret
)

"""Gets and returns formatted TOP posts (and related comments) by subreddit

    Args:
        subreddit (str): the subreddit we want to scrape posts for

    Returns:
        content_dict: a dictionary of subreddit submission dictionaries. ID as the key and relevant data stored as the value.
"""
def get_top_posts(subreddit, limit=None):
    submissions = reddit.subreddit(subreddit).top("all", limit=limit)
    post_dict = {}
    for sub in submissions:
        current_ID = sub.id
        sub_dict = {}
        sub_dict['num_comments'] = sub.num_comments
        sub_dict['score'] = sub.score
        sub_dict['selftext'] = sub.selftext
        sub_dict['stickied'] = sub.stickied
        sub_dict['title'] = sub.title
        sub_dict['upvote_ratio'] = sub.upvote_ratio
        sub_dict['created_utc'] = sub.created_utc
        sub_dict['year'] = datetime.date.fromtimestamp(sub.created_utc).year

        current_top_comments = []
        # Set comment sort to best before retrieving comments
        # The appropriate values for comment_sort include confidence, controversial, new, old, q&a, and top
        sub.comment_sort = 'top' 
        # Limit to, at most, 10 top level comments
        sub.comment_limit = 10
        for top_level_comment in sub.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            current_top_comments.append(top_level_comment.body)
        
        sub_dict['top_comments'] = current_top_comments

        post_dict[current_ID] = sub_dict
    
    return post_dict

"""Gets and returns formatted CONTROVERSIAL posts (and related comments) by subreddit

    Args:
        subreddit (str): the subreddit we want to scrape posts for

    Returns:
        content_dict: a dictionary of subreddit submission dictionaries. ID as the key and relevant data stored as the value.
"""
def get_controversial_posts(subreddit, limit=None):
    submissions = reddit.subreddit(subreddit).controversial("all", limit=limit)
    post_dict = {}
    for sub in submissions:
        current_ID = sub.id
        sub_dict = {}
        sub_dict['num_comments'] = sub.num_comments
        sub_dict['score'] = sub.score
        sub_dict['selftext'] = sub.selftext
        sub_dict['stickied'] = sub.stickied
        sub_dict['title'] = sub.title
        sub_dict['upvote_ratio'] = sub.upvote_ratio
        sub_dict['created_utc'] = sub.created_utc
        sub_dict['year'] = datetime.date.fromtimestamp(sub.created_utc).year

        current_top_comments = []
        # Set comment sort to best before retrieving comments
        # The appropriate values for comment_sort include confidence, controversial, new, old, q&a, and top
        sub.comment_sort = 'top' 
        # Limit to, at most, 10 top level comments
        sub.comment_limit = 10
        for top_level_comment in sub.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            current_top_comments.append(top_level_comment.body)
        
        sub_dict['top_comments'] = current_top_comments

        post_dict[current_ID] = sub_dict
    
    return post_dict

"""Gets and returns formatted HOT posts (and related comments) by subreddit

    Args:
        subreddit (str): the subreddit we want to scrape posts for

    Returns:
        content_dict: a dictionary of subreddit submission dictionaries. ID as the key and relevant data stored as the value.
"""
def get_hot_posts(subreddit, limit=None):
    submissions = reddit.subreddit(subreddit).hot(limit=limit)
    post_dict = {}
    for sub in submissions:
        current_ID = sub.id
        sub_dict = {}
        sub_dict['num_comments'] = sub.num_comments
        sub_dict['score'] = sub.score
        sub_dict['selftext'] = sub.selftext
        sub_dict['stickied'] = sub.stickied
        sub_dict['title'] = sub.title
        sub_dict['upvote_ratio'] = sub.upvote_ratio
        sub_dict['created_utc'] = sub.created_utc
        sub_dict['year'] = datetime.date.fromtimestamp(sub.created_utc).year

        current_top_comments = []
        # Set comment sort to best before retrieving comments
        # The appropriate values for comment_sort include confidence, controversial, new, old, q&a, and top
        sub.comment_sort = 'top' 
        # Limit to, at most, 10 top level comments
        sub.comment_limit = 10
        for top_level_comment in sub.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            current_top_comments.append(top_level_comment.body)
        
        sub_dict['top_comments'] = current_top_comments

        post_dict[current_ID] = sub_dict
    
    return post_dict

# TODO: include functions to grab through random and search requests - will be able to give us posts not found above
# NOTE: its more difficult because random only returns one at a time so we might have to send requests 
# and fill in as necessary, keeping in mind the 2 second request interval
# NOTE: search requests will be difficult too because we need to know what we're searching for
# NOTE: we have to consider this because the Reddit API no longer allows queries within a timeframe,
# plus it only allows for 1000 submissions per above queries.

def main():
    post_dict = get_top_posts('learnpython', 1)
    print(post_dict)
    post_dict = get_controversial_posts('learnpython', 1)
    print(post_dict)
    post_dict = get_hot_posts('learnpython', 1)
    print(post_dict)


if __name__ == "__main__":
    main()