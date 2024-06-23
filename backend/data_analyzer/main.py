import sys, os, time, uvicorn
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager
from components.scheduler import Scheduler
from modal import Image, App, asgi_app

def example_task():
    print("starting data analysis.")
    #todo - data collection happens here
    time.sleep(5)

    print("completed data analysis.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start the analyzing task
    task_scheduler = Scheduler(interval=10, task=example_task)
    task_scheduler.start()
    yield
    # stop the analyzing task
    task_scheduler.stop()

data_analyzer_app = FastAPI(lifespan=lifespan)



@data_analyzer_app.get("/")
def read_root():
    return {"Hello": "data_analyzer_app"}


#MODAL DEPLOYMENT
app = App("data_analyzer")

image = Image.debian_slim()

@app.function(image=image)
@asgi_app()
def fastapi_app():
    return data_analyzer_app