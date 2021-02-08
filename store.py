import datetime

from scrape import get_subreddit_meta, get_top_posts, get_hot_posts, get_controversial_posts

from mongoengine import *
db = connect('reddalysis', host='localhost', port=27017)

# Subreddit class to store all necessary metadata regarding the subreddit
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

# Use only if you want to refresh your database
def clear_db():
    db.drop_database('reddalysis')  

def insert_subreddit(data_dict):
    curr_subreddit = Subreddit(
        subreddit_id = data_dict['id'],
        created_utc =  data_dict['created_utc'],
        year =  data_dict['year'],
        description =  data_dict['description'],
        display_name =  data_dict['display_name'],
        name =  data_dict['name'],
        subscribers =  data_dict['subscribers'],
        public_description =  data_dict['public_description'],
        added = datetime.datetime.now
    ).save()

    return curr_subreddit

def insert_submissions(subreddit, post_dict):
    for submission_id in post_dict:
        data_dict = post_dict[submission_id]
        Submission(
            submission_id = submission_id,
            num_comments = data_dict['num_comments'],
            score = data_dict['score'],
            selftext = data_dict['selftext'],
            stickied = data_dict['stickied'],
            title = data_dict['title'],
            upvote_ratio = data_dict['upvote_ratio'],
            created_utc = data_dict['created_utc'],
            year = data_dict['year'],
            subreddit = subreddit,
            top_comments = data_dict['top_comments'],
            added = datetime.datetime.now
        ).save()


# TODO: Add comments, arguments for command line, tags for submissions, error handling for already written posts
# TODO: Add documentation for how to save data and what to expect if there's already something there
def main():
    clear_db()

    sub_dict = get_subreddit_meta('learnpython')
    curr_subreddit = insert_subreddit(sub_dict)

    # for subr in Subreddit.objects:
    #     print(subr.display_name)
    #     print(subr.subscribers)

    # user_obj = User.objects(first_name='mr')
    # for sub in user_obj:
    #     print(curr_user.last_name)


    post_dict = get_top_posts('learnpython', 3, 'year')
    insert_submissions(curr_subreddit, post_dict)

    for subm in Submission.objects:
        print(subm.title)
        print(subm.score)

if __name__ == "__main__":
    main()