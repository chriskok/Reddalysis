# Reddalysis
Project to investigate the history of selected subreddits with data science and machine learning

## Requirements
- [Python](https://www.python.org/downloads/)
- [MongoDB](https://docs.mongodb.com/manual/administration/install-community/)
- Python libraries in requirement.txt

## Usage
- go to https://www.reddit.com/prefs/apps to register your app; keep the app client ID and secret
- duplicate 'example.config' and rename to 'client.config'; change the client ID and secret to your own app's codes 
- get and store desired data: `python store.py -s <SUBREDDIT>` 
  - e.g. `python store.py -s learnpython`

## Database Commands
- Clear the entire database: `python store.py -c` 
- Delete all saved posts related to a specific Subreddit: `python store.py -d <SUBREDDIT>` 
  - e.g. `python store.py -d learnpython` 
- Limit the amount of data collected: `python store.py -l <LIMIT> -s <SUBREDDIT>` 
  - e.g. `python store.py -l 15 -s learnpython`