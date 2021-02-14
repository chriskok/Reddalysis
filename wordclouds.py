import matplotlib.pyplot as plt
import numpy as np
import pickle
import argparse
from os import path

import re, string, unicodedata
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Get the necessary class structure and connect to the DB
from db_config import Subreddit, Submission
from mongoengine import *
db = connect('reddalysis', host='localhost', port=27017)

############################################
########## DATA HELPER FUNCTIONS ###########
############################################

def get_submissions(subreddit_name):
    data_path = 'data/{}_top.pickle'.format(subreddit_name)
    if (not path.exists(data_path)): 
        print("ERROR: Files for r/{} not found. Please run \'python store.py -s {} -p\' first.".format(subreddit_name, subreddit_name))
        return None

    full_post_dict = {}
    # USING PICKLE FILES
    with open('data/{}_top.pickle'.format(subreddit_name), 'rb') as handle:
        full_post_dict.update(pickle.load(handle))
    with open('data/{}_hot.pickle'.format(subreddit_name), 'rb') as handle:
        full_post_dict.update(pickle.load(handle))
    with open('data/{}_random.pickle'.format(subreddit_name), 'rb') as handle:
        full_post_dict.update(pickle.load(handle))
    with open('data/{}_controversial.pickle'.format(subreddit_name), 'rb') as handle:
        full_post_dict.update(pickle.load(handle))
    
    print('Loaded {} submissions'.format(len(list(full_post_dict.keys()))))

    return full_post_dict


############################################
####### TEXT PREPROCESSING FUNCTIONS #######
############################################

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def remove_hyperlinks(words):
    """Remove hyperlinks from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'^https?:\/\/.*[\r\n]*', '', word)
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def normalize(words):
    words = remove_hyperlinks(words)
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_stopwords(words)
    return words

def bag_of_words(words):
    word2count = {} 
    for word in words: 
        if word not in word2count.keys(): 
            word2count[word] = 1
        else: 
            word2count[word] += 1

    return word2count

############################################
############## MAIN FUNCTIONS ##############
############################################

def process_bow(words):
    words = nltk.word_tokenize(words)
    words = normalize(words)
    bow = bag_of_words(words)

    return bow

def subreddit_to_bow(subreddit_name):
    full_post_dict = get_submissions(subreddit_name)
    if (full_post_dict is None): return

    full_text = ""
    for post in full_post_dict:
        curr_post = full_post_dict[post]
        full_text = full_text + curr_post['title'] + " " + curr_post['selftext'] + " " + ' '.join(curr_post['top_comments']) + " "
    
    bow = process_bow(full_text)
    with open('./data/{}_{}.pickle'.format(subreddit_name, 'bow'), 'wb') as handle:
        pickle.dump(bow, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print('created bow file for: {}'.format(subreddit_name))

    return process_bow(full_text)

def subreddit_to_yearly_bow(subreddit_name):
    full_post_dict = get_submissions(subreddit_name)
    if (full_post_dict is None): return

    yearly_texts = {}
    for post in full_post_dict:
        curr_post = full_post_dict[post]
        year = curr_post['year']
        curr_text = curr_post['title'] + " " + curr_post['selftext'] + " " + ' '.join(curr_post['top_comments']) + " "
        if year not in yearly_texts.keys(): 
            yearly_texts[year] = curr_text
        else: 
            yearly_texts[year] = yearly_texts[year] + curr_text
    
    yearly_bow = {}
    for year in yearly_texts:
        yearly_bow[year] = process_bow(yearly_texts[year])

    with open('./data/{}_{}.pickle'.format(subreddit_name, 'yearly_bow'), 'wb') as handle:
        pickle.dump(yearly_bow, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print('created yearly bow file for: {}'.format(subreddit_name))

    return yearly_bow

def get_bow(subreddit_name):
    data_path = 'data/{}_bow.pickle'.format(subreddit_name)
    if (not path.exists(data_path)): subreddit_to_bow(subreddit_name)
    with open(data_path, 'rb') as handle:
        return pickle.load(handle)

def get_yearly_bow(subreddit_name):
    data_path = 'data/{}_yearly_bow.pickle'.format(subreddit_name)
    if (not path.exists(data_path)): subreddit_to_yearly_bow(subreddit_name)
    with open(data_path, 'rb') as handle:
        return pickle.load(handle)

def main():
    # # USING MONGODB

    # # Prints all submissions text that has score greater than 5000
    # # More querying documentation: https://docs.mongoengine.org/guide/querying.html
    # for subm in Submission.objects(score__gt=5000):
    #     print('score: {}, title: {}'.format(subm.score, subm.title))
    
    # # Save the year of all collected posts and plot that as a histogram
    # year_array = []
    # for subm in Submission.objects:
    #     year_array.append(subm.year)

    # y = np.array(year_array)
    # plt.hist(y)
    # plt.show()

    # # USING PICKLE FILES
    # full_post_dict = get_submissions('learnmachinelearning')

    # year_array = []
    # for item in full_post_dict:
    #     year_array.append(full_post_dict[item]['year'])
    
    # y = np.array(year_array)
    # plt.hist(y)
    # plt.show()

    subreddit_name = args.subreddit

    # To create the BOW pickle files
    subreddit_to_bow(subreddit_name)
    subreddit_to_yearly_bow(subreddit_name)

    # # To get the saved BOWs
    # print(get_bow('learnmachinelearning'))
    # print(get_yearly_bow('learnmachinelearning')[2016])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--subreddit', help="subreddit to scrape and store data from")
    args = parser.parse_args()
    main()