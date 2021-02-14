# Reddalysis
Project to investigate the history of selected subreddits with data science and machine learning

## Requirements
- [Python](https://www.python.org/downloads/)
- [MongoDB](https://docs.mongodb.com/manual/administration/install-community/)
- [NodeJS](https://nodejs.org/en/download/)
- Python libraries in requirement.txt

## Usage
- go to https://www.reddit.com/prefs/apps to register your app; keep the app client ID and secret
- duplicate 'example.config' and rename to 'client.config'; change the client ID and secret to your own app's codes 
- get and store desired data (as pickle files): `python store.py -s <SUBREDDIT> -p` 
  - e.g. `python store.py -s learnpython -p`
- preprocess the data (right now it's just with wordclouds): `python wordclouds.py -s <SUBREDDIT>`
  - e.g. `python wordclouds.py -s learnpython`
- start the API: `uvicorn api:app --reload`
- start the node webserver: `npm start`
  - If it's your first time, install the necessary node dependencies: `npm install`

## Database Commands
- Clear the entire database: `python store.py -c` 

- Delete all saved posts related to a specific Subreddit: `python store.py -d <SUBREDDIT>` 
  - e.g. `python store.py -d learnpython` 

- Limit the amount of data collected: `python store.py -l <LIMIT> -s <SUBREDDIT>` 
  - e.g. `python store.py -l 15 -s learnpython`

- Limit the time range of data collected: `python store.py -t <TIME LIMIT> -s <SUBREDDIT>` 
  - e.g. `python store.py -t year -s learnpython`

- Save the data as pickle files: `python store.py -p -s <SUBREDDIT>` 
  - e.g. `python store.py -p -s learnpython`


## Environment Set Up
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Deployment Details
- API deployed on Heroku
  - To make changes, commit them with git and then: `git push heroku HEAD:master`
  - For terminal access on heroku server: `heroku run bash -a reddalysis`
  - For error logs: `heroku logs --tail `
- Webserver deployed on Github Pages