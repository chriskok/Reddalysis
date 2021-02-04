import praw
import configparser
import time
from datetime import datetime
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

# NOTE: the below no longer works because of recent changes to the Reddit API

# submissions = reddit.subreddit('learnpython').hot(limit=5)
# submissions = reddit.subreddit('learnpython').top("all")

# for sub in submissions:
#     print('TITLE: {}'.format(sub.title))
#     print('SCORE: {}'.format(sub.score))
#     # print('TEXT: {}'.format(sub.selftext))
#     # for top_level_comment in sub.comments:
#     #     if isinstance(top_level_comment, MoreComments):
#     #         continue
#     #     print(top_level_comment.body)

# current_timestamp = time.time()
# 60 seconds * 60 minutes * 24 hours * 60 days = 2 months
# two_months_timestamp = current_timestamp - (60 * 60 * 24 * 60)
# query = 'timestamp:{}..{}'.format(current_timestamp, two_months_timestamp)
# results = reddit.subreddit('test').search(query, sort='new')

# search_results = list(submissions_between(
#     reddit,
#     'learnpython',lowest_timestamp=two_months_timestamp
#     )
# )

# for sub in search_results:
#     print('TITLE: {}'.format(sub.title))
#     print('SCORE: {}'.format(sub.score))

# import datetime
# params = {'sort':'new', 'limit':None}
# time_now = datetime.datetime.now()
# test_search = reddit.subreddit('learnpython').search('timestamp:{0}..{1}'.format(
#     int((time_now - datetime.timedelta(days=365)).timestamp()),
#     int(time_now.timestamp())),
#     **params)

# print(len(list(test_search)))


# NOTE: Found out that PRAW/Reddit API no longer supports queries for submissions between two timestamps.
# Will try working around this issue by getting top comments of all time and sorting by year.

# NOTE: Also found out the limit of the top submissions is ~1000. Thinking now about grabbing the most 
# controversial, hot, random, search. 

submissions = reddit.subreddit('learnpython').top("all", limit=None)
year_array = []

for sub in submissions:
    # print('TITLE: {}'.format(sub.title))
    # print('SCORE: {}'.format(sub.score))
    # print('TIME: {}'.format(time.ctime(sub.created_utc)))

    # timestamp = datetime.date.fromtimestamp(sub.created_utc).strftime('%Y-%m-%d %H:%M:%S')
    # print(timestamp)

    year = datetime.date.fromtimestamp(sub.created_utc).year
    year_array.append(year)

print(len(year_array))

import matplotlib.pyplot as plt
import numpy as np

y = np.array(year_array)
plt.hist(y)
plt.show()