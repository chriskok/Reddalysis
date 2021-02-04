import praw
import configparser

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

submission = reddit.submission(id="3g1jfi")

submissions = reddit.subreddit('learnpython').hot(limit=5)


for top_level_comment in submission.comments:
    print(top_level_comment.body)