# https://fastapi.tiangolo.com/tutorial/
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from wordclouds import get_bow, get_yearly_bow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='https?://.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
   return {"message": "Hello World"}

@app.get("/api/v1/get_bow")
async def bow(subreddit_name: str):    
    if subreddit_name:
        return JSONResponse(content=get_bow(subreddit_name), status_code=200)

    return JSONResponse(content={"Error": "The subreddit name is missing"}, status_code=400)

@app.get("/api/v1/get_yearly_bow")
async def yearly_bow(subreddit_name: str):    
    if subreddit_name:
        return JSONResponse(content=get_yearly_bow(subreddit_name), status_code=200)

    return JSONResponse(content={"Error": "The subreddit name is missing"}, status_code=400)