import datetime
import argparse

from scrape import get_subreddit_meta, get_top_posts, get_hot_posts, get_controversial_posts, get_random_posts
from db_config import Subreddit, Submission
from mongoengine import *
db = connect('reddalysis', host='localhost', port=27017)

# Use only if you want to refresh your database
def clear_db():
    db.drop_database('reddalysis')  

"""Insert metadata dictionary for a specific subreddit into the database

    Args:
        data_dict (dict): a dictionary of relevant metadata for the subreddit

    Returns:
        curr_subreddit: reference to the created Subreddit document
"""
def insert_subreddit(data_dict):
    try:
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
    except NotUniqueError:
        print("{} already in DB".format(data_dict['display_name']))
        curr_subreddit = Subreddit.objects(subreddit_id=data_dict['id']).first()

    return curr_subreddit

"""Insert data dictionary for a post into the database

    Args:
        subreddit (Subreddit): a reference to the created Subreddit document
        data_dict (dict): a dictionary of relevant information for this submission

    Returns:
        duplicate (int): whether or not the current post is already in the DB (1 if duplicated, 0 otherwise)
"""
def insert_submission(subreddit, data_dict):
    try:
        Submission(
            submission_id = data_dict['id'],
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
    except NotUniqueError:
        return 1
    
    return 0

"""Insert all data from a particular subreddit into the DB

    Args:
        subreddit (Subreddit): a reference to the created Subreddit document
        post_dict (dict): a dictionary of subreddit submission dictionaries.

    Returns:
        duplicate_count (int): a total count of how many duplicates there were
"""
def insert_submissions(subreddit, post_dict):
    duplicate_count = 0
    for submission_id in post_dict:
        data_dict = post_dict[submission_id]
        duplicate_count += insert_submission(subreddit, data_dict)

    return duplicate_count

# TODO: Add options to choose between TOP, CONTRO and HOT or all three.
# TODO: Add tags to the posts to know if these posts were taken from TOP, HOT, by year, etc.
def main():

    if args.clear:
        clear_db()
        print('Cleared full database')
        return
    
    if args.delete is not None:
        subr = Subreddit.objects(display_name__iexact=args.delete).first()
        delete_count = 0
        for subm in Submission.objects(subreddit=subr):
            subm.delete()
            delete_count += 1
        print('Deleted {} submissions from r/{}'.format(delete_count, args.delete))
        return

    subreddit_name = args.subreddit
    fetch_limit = args.limit
    time_range = args.time

    # Store current subreddit
    sub_dict = get_subreddit_meta(subreddit_name)
    curr_subreddit = insert_subreddit(sub_dict)

    duplicate_count = 0
    scraped_count = 0

    # Store top submissions
    post_dict = get_top_posts(subreddit_name, fetch_limit, time_range)
    scraped_count += len(post_dict)
    duplicate_count += insert_submissions(curr_subreddit, post_dict)

    # Store hot submissions
    post_dict = get_hot_posts(subreddit_name, fetch_limit)
    scraped_count += len(post_dict)
    duplicate_count += insert_submissions(curr_subreddit, post_dict)

    # Store controversial submissions
    post_dict = get_controversial_posts(subreddit_name, fetch_limit, time_range)
    scraped_count += len(post_dict)
    duplicate_count += insert_submissions(curr_subreddit, post_dict)

    # Store random submissions
    random_limit = fetch_limit if fetch_limit is not None else 1000
    post_dict = get_random_posts(subreddit_name, random_limit)
    scraped_count += len(post_dict)
    duplicate_count += insert_submissions(curr_subreddit, post_dict)

    if (duplicate_count > 0): print("Skipped {} posts already in DB".format(duplicate_count))

    if (fetch_limit is not None): print('Added {} new posts to the DB'.format(scraped_count - duplicate_count))
    else: print('Added {} new posts to the DB'.format(scraped_count * 1000 - duplicate_count))

    # for subm in Submission.objects:
    #     print(subm.title)
    #     print(subm.score)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delete', default=None, help="delete all data from a specific subreddit")
    parser.add_argument('-c', '--clear', default=False, action="store_true", help="fully clear the database before starting")
    parser.add_argument('-l', '--limit', type=int, default=None, help="limit to number of posts")
    parser.add_argument('-s', '--subreddit', help="subreddit to scrape and store data from")
    parser.add_argument('-t', '--time', default='all', help="time range to grab top and controversial posts from [all, day, hour, month, week, year]")
    args = parser.parse_args()

    main()