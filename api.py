# https://fastapi.tiangolo.com/tutorial/
from fastapi import FastAPI, Form
import sqlalchemy
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='https?://.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://www.cdata.com/kb/tech/mongodb-python-sqlalchemy.rst
# engine = create_engine("mongodb///?Server=MyServer&Port=27017&Database=test&User=test&Password=Password")

# auto generated docs: http://127.0.0.1:8000/docs#/

@app.get("/")
async def root():
   return {"message": "Hello World"}

@app.get("/subreddit_data")
async def get_subreddit_data(subreddit: str = Form(...), year: int = Form(...)):
   pass

# some changes