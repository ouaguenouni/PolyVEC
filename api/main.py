from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/randPos")
async def randPos():
    return {"message": random.randrange(0,577)}