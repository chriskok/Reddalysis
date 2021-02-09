from fastapi import FastAPI, Form
import sqlalchemy
from sqlalchemy import create_engine

app = FastAPI()

# https://www.cdata.com/kb/tech/mongodb-python-sqlalchemy.rst
engine = create_engine("mongodb///?Server=MyServer&Port=27017&Database=test&User=test&Password=Password")

@app.get("/")
async def root():
   return {"message": "Hello World"}

@app.get("/subreddit_data")
async def get_subreddit_data(subreddit: str = Form(...), year: int = Form(...)):
   pass
