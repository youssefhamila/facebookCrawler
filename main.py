from importlib.resources import path
import uvicorn
from facebookCrawler import *
from fastapi import FastAPI, Response
from dataBase import showAll
import pandas as pd


app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello World"}
@app.get("/collect/{scrol}")
def scrape(scrol:int):
    AccessUrl(url="https://www.facebook.com/Meta/",scrol=scrol)
    return {"message": "https://www.facebook.com/Meta/ scrapped"}
@app.get("/collect/")
def scrapeall():
    AccessUrl(url="https://www.facebook.com/Meta/")
    return {"message": "https://www.facebook.com/Meta/ scrapped"}
@app.get("/show")
def show():
    return showAll()




if __name__ == '__main__':
    uvicorn.run(app , port=8000, host="0.0.0.0")