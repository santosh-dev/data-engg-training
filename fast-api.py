#pip install fastapi

#pip install uvicorn

from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "welcome to fast api"

