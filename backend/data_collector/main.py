import sys, os, time
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager
from components.scheduler import Scheduler
from modal import Image, App, asgi_app





# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # start the collector task
#     task_scheduler = Scheduler(interval=10, task=example_task)
#     task_scheduler.start()
#     yield
#     # stop the collector task
#     task_scheduler.stop()

data_collector_app = FastAPI()

def example_task():
    print("starting data analysis.")
    #todo - data collection happens here
    time.sleep(0.5)

    return {"detail": "completed data analysis."}

@data_collector_app.get("/")
def read_root():
    return example_task()
    


@data_collector_app.get("/health")
def health_check():
    return {"detail": "I am healthy"}

#MODAL DEPLOYMENT
app = App("data_collector")

image = Image.debian_slim()

@app.function(image=image)
@asgi_app()
def fastapi_app():
    return data_collector_app