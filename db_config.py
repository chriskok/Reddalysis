
import datetime
from mongoengine import *
db = connect('reddalysis', host='localhost', port=27017)

# Subreddit class to store all necessary metadata regarding the subreddit
# Refer here for possible fields: https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html
class Subreddit(Document):
    subreddit_id = StringField(required=True, unique=True)
    created_utc = FloatField()
    year = IntField()
    description = StringField()
    display_name = StringField(required=True)
    name = StringField(required=True)
    subscribers = IntField()
    public_description = StringField()
    added = DateTimeField(default=datetime.datetime.now)

# Submission class to store all relevant data to the post
# Refer here for possible fields: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
class Submission(Document):
    submission_id = StringField(required=True, unique=True)
    num_comments = IntField()
    score = IntField()
    selftext = StringField(required=True)
    stickied = BooleanField()
    title = StringField(required=True)
    upvote_ratio = FloatField()
    created_utc = FloatField()
    year = IntField()
    subreddit = ReferenceField(Subreddit)
    top_comments = ListField(StringField())
    added = DateTimeField(default=datetime.datetime.now)