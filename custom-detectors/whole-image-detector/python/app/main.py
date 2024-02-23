# from typing import Any
from logging import getLogger, StreamHandler

from fastapi import FastAPI
from pydantic import BaseModel

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")

class Data(BaseModel):
    image_data: str


app = FastAPI()


@app.get("/health")
def health_check():
    logger.info(f"Health check: ok")
    return {"health": "ok"}


@app.post("/whole-image-detection")
def whole_box_detection(data: Data):
    response = {
        "boxes": [
            [0.1,0.1,0.9,0.9]
        ]
    }
    return response
