# https://fastapi.tiangolo.com/tutorial/
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/api/v1/recommendations")
async def recommendations(anime_code: int = Query(""), n_recommendations: int = Query(5)):    
    if anime_code:
        recommendations = obtain_recommendations(anime_code, n_recommendations)
        return JSONResponse(content=recommendations, status_code=200)

    return JSONResponse(content={"Error": "The anime code is missing"}, status_code=400)