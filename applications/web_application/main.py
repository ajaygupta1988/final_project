from typing import Union

from fastapi import FastAPI

web_app = FastAPI()


@web_app.get("/")
def read_root():
    return {"Hello": "World"}


@web_app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}