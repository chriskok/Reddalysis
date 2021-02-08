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

"""Gets and returns formatted subreddit metadata

    Args:
        subreddit (str): the subreddit we want to get metadata for 

    Returns:
        subreddit_dict: a dictionary of relevant metadata for the subreddit
"""
def get_subreddit_meta(subreddit):
    subreddit_dict = {}
    subreddit = reddit.subreddit(subreddit)
    
    subreddit_dict['id'] = subreddit.id
    subreddit_dict['created_utc'] = subreddit.created_utc
    subreddit_dict['year'] = datetime.date.fromtimestamp(subreddit.created_utc).year
    subreddit_dict['description'] = subreddit.description
    subreddit_dict['display_name'] = subreddit.display_name
    subreddit_dict['name'] = subreddit.name
    subreddit_dict['subscribers'] = subreddit.subscribers
    subreddit_dict['public_description'] = subreddit.public_description

    return subreddit_dict

"""Extracts and processes relevant information for a submission

    Args:
        sub (Submission): the submission we're extracting data from
        comment_sort (str): sorting order for comments [confidence, controversial, new, old, q&a, top]

    Returns:
        sub_dict: a dictionary of relevant information for this submission
"""
def save_submission(sub, comment_sort='top'):
    sub_dict = {}
    sub_dict['id'] = sub.id
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
    sub.comment_sort = comment_sort 
    # Limit to, at most, 10 top level comments
    sub.comment_limit = 10
    for top_level_comment in sub.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        current_top_comments.append(top_level_comment.body)
    
    sub_dict['top_comments'] = current_top_comments

    return sub_dict

"""Gets and returns formatted TOP posts (and related comments) by subreddit

    Args:
        subreddit (str): the subreddit we want to scrape posts for
        limit (int): limit to the number of submissions
        time_range (str): how far back to look for gathering data [all, day, hour, month, week, year]

    Returns:
        content_dict: a dictionary of subreddit submission dictionaries. ID as the key and relevant data stored as the value.
"""
def get_top_posts(subreddit, limit=None, time_range="all"):
    submissions = reddit.subreddit(subreddit).top(time_range, limit=limit)
    post_dict = {}
    for sub in submissions:
        current_ID = sub.id
        sub_dict = save_submission(sub)
        post_dict[current_ID] = sub_dict
    
    return post_dict

"""Gets and returns formatted CONTROVERSIAL posts (and related comments) by subreddit

    Args:
        subreddit (str): the subreddit we want to scrape posts for
        limit (int): limit to the number of submissions
        time_range (str): how far back to look for gathering data [all, day, hour, month, week, year]

    Returns:
        content_dict: a dictionary of subreddit submission dictionaries. ID as the key and relevant data stored as the value.
"""
def get_controversial_posts(subreddit, limit=None, time_range="all"):
    submissions = reddit.subreddit(subreddit).controversial(time_range, limit=limit)
    post_dict = {}
    for sub in submissions:
        current_ID = sub.id
        sub_dict = save_submission(sub)
        post_dict[current_ID] = sub_dict
    
    return post_dict

"""Gets and returns formatted HOT posts (and related comments) by subreddit

    Args:
        subreddit (str): the subreddit we want to scrape posts for
        limit (int): limit to the number of submissions
        time_range (str): how far back to look for gathering data [all, day, hour, month, week, year]

    Returns:
        content_dict: a dictionary of subreddit submission dictionaries. ID as the key and relevant data stored as the value.
"""
def get_hot_posts(subreddit, limit=None):
    submissions = reddit.subreddit(subreddit).hot(limit=limit)
    post_dict = {}
    for sub in submissions:
        current_ID = sub.id
        sub_dict = save_submission(sub)
        post_dict[current_ID] = sub_dict
    
    return post_dict

# TODO: include functions to grab through random and search requests - will be able to give us posts not found above
# NOTE: its more difficult because random only returns one at a time so we might have to send requests 
# and fill in as necessary, keeping in mind the 2 second request interval
# NOTE: search requests will be difficult too because we need to know what we're searching for
# NOTE: we have to consider this because the Reddit API no longer allows queries within a timeframe,
# plus it only allows for 1000 submissions per above queries.

def main():
    post_dict = get_top_posts('learnpython', 1, 'month')
    print(post_dict)
    # post_dict = get_controversial_posts('learnpython', 1)
    # print(post_dict)
    # post_dict = get_hot_posts('learnpython', 1)
    # print(post_dict)

    # sub_dict = get_subreddit_meta('learnpython')
    # print(sub_dict)

if __name__ == "__main__":
    main()