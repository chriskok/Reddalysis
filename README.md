# Reddalysis
Project to investigate the history of selected subreddits with data science and machine learning

## Requirements
- praw
- configparser
- mongoengine

## Usage
- go to https://www.reddit.com/prefs/apps to register your app; keep the app client ID and secret
- duplicate 'example.config' and rename to 'client.config'; change the client ID and secret to your own app's codes 
- run any of the scripts in the repository:
  - e.g ```python scraping.py```