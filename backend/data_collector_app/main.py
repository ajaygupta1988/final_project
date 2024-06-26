import sys, os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import make_asgi_app
import modal

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from components import QueryManager, ExternalDataFetcher, MessagingQueue
from schemas import ExternalResponseDataSchema
from config import settings

data_collector_app = FastAPI()

instrumentator = Instrumentator().instrument(data_collector_app)

data_collector_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start instrumenting prometheus
    instrumentator.expose(app)
    yield
    # do something on application stop


@data_collector_app.get("/")
def health_check():
    return {"detail": "I am a healthy data collector."}


@data_collector_app.get(
    "/load_symbol_data",
    description="API endpoint to listen to save stock ticker data requests in mongo database. The symbol will be recoverd from the queue, this is simply a ping that a new message is waiting for you to process. Constant running server is much better option for fast polling, but for the purpose of this project I kept it simple.",
)
async def load_symbol_data():
    try:
        # Messaging queue consumer to get the symbol value from the queue.
        message_queue = MessagingQueue()
        message = message_queue.recieve_message()
        if len(message) > 0:
            receipt_handle = message[0]["ReceiptHandle"]
            symbol = message[0]["Body"]

            mongo_query_manager = QueryManager()
            update_required = (
                await mongo_query_manager.check_if_data_is_missing_or_stale(
                    symbol=symbol
                )
            )

            if update_required is True:
                data_fetcher = ExternalDataFetcher()
                vantage_api_response_data = await data_fetcher.get_data_for_symbol(
                    symbol=symbol
                )
                result = await mongo_query_manager.add_data_from_api(
                    data=ExternalResponseDataSchema(**vantage_api_response_data)
                )
            message_queue.delete_message(receipt_handle)
            print(
                {
                    "detail": f"Data succesfully loaded for {symbol} and message from the queue is deleted"
                }
            )
            return {
                "detail": f"Data succesfully loaded for {symbol} and message from the queue is deleted"
            }
        else:
            print({"detail": "No message received. wrong call"})
    except Exception as e:
        print(str(e))
        raise HTTPException(message="Error occured", status_code=500)


# Prometheus Metrics
metrics_app = make_asgi_app()
data_collector_app.mount("/metrics", metrics_app)

# MODAL CLOUD DEPLOYMENT ATTRIBUTES: Basically we are attaching our app instance to modal serverless function. (No impact on local running)
app = modal.App("data_collector")

vol = modal.Volume.from_name("my-volume", create_if_missing=True)

# defining requirements for the serverless function
image = modal.Image.debian_slim(python_version="3.10.11").pip_install(
    [
        "cython<3.0.0",
        "PyYAML==6.0.1",
        "fastapi",
        "modal",
        "requests",
        "prometheus-fastapi-instrumentator",
        "pymongo[srv]",
        "motor",
        "pandas",
        "pydantic-settings",
        "boto3",
    ]
)


# attaching app to serverless function
@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("aws-access"),
        modal.Secret.from_name("mongodb-secret"),
        modal.Secret.from_name("vantage_api_key"),
        modal.Secret.from_name("messaging-secrets"),
    ],
)
@modal.asgi_app()
def fastapi_app():
    return data_collector_app
