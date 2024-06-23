import sys
import os


data_analyzer_app = FastAPI()


@data_analyzer_app.get("/")
def read_root():
    return {"Hello": "World"}


@data_analyzer_app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(read_root, host="0.0.0.0", port=8001)