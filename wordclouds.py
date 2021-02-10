import matplotlib.pyplot as plt
import numpy as np
import pickle

# Get the necessary class structure and connect to the DB
from db_config import Subreddit, Submission
from mongoengine import *
db = connect('reddalysis', host='localhost', port=27017)

def main():
    # USING MONGODB

    # Prints all submissions text that has score greater than 5000
    # More querying documentation: https://docs.mongoengine.org/guide/querying.html
    for subm in Submission.objects(score__gt=5000):
        print('score: {}, title: {}'.format(subm.score, subm.title))
    
    # Save the year of all collected posts and plot that as a histogram
    year_array = []
    for subm in Submission.objects:
        year_array.append(subm.year)

    y = np.array(year_array)
    plt.hist(y)
    plt.show()

    # USING PICKLE FILES
    with open('data/python_top.pickle', 'rb') as handle:
        post_dict = pickle.load(handle)

    year_array = []
    print(post_dict)
    for item in post_dict:
        year_array.append(post_dict[item]['year'])
    
    y = np.array(year_array)
    plt.hist(y)
    plt.show()

if __name__ == "__main__":
    main()