import sys, os, time, uvicorn
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager
from components.scheduler import Scheduler

def example_task():
    print("starting data analysis.")
    #todo - data collection happens here
    time.sleep(5)

    print("completed data analysis.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start the collector task
    task_scheduler = Scheduler(interval=10, task=example_task)
    task_scheduler.start()
    yield
    # stop the collector task
    task_scheduler.stop()

data_collector_app = FastAPI(lifespan=lifespan)



@data_collector_app.get("/")
def read_root():
    return {"Hello": "World"}


@data_collector_app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



if __name__ == "__main__":
    uvicorn.run(data_collector_app, host="0.0.0.0", port=8001)