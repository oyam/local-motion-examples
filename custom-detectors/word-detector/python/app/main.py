# from typing import Any
from logging import getLogger, StreamHandler

from fastapi import FastAPI
from pydantic import BaseModel

from .word_detector import WordDetector

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


class Data(BaseModel):
    image_data: str


app = FastAPI()
word_detector = WordDetector()


@app.get("/health")
def health_check():
    logger.info(f"Health check: ok")
    return {"health": "ok"}


@app.post("/word-detection")
def word_detection(data: Data):
    boxes = word_detector.detect(data.image_data)
    response = {"boxes": boxes}
    return response
