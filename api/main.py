from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/api/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/randPos")
async def randPos():
    return {random.randrange(0,577)}
