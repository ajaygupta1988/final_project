import sys, os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import make_asgi_app
import requests
import modal

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from components import ExternalDataFetcher, QueryManager, Utils, MessagingQueue
from schemas import (
    SymbolLookUpResponse,
    ExternalResponseDataSchema,
    EfficientDataResponse,
    MetaDataSchema,
)
from config import settings


data_analyzer_app = FastAPI()

data_analyzer_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

instrumentator = Instrumentator().instrument(data_analyzer_app)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start instrumenting prometheus
    instrumentator.expose(app)
    yield
    # do something on application stop


@data_analyzer_app.get("/")
def health_check():
    return {"detail": "I am a healthy data analyzer."}


@data_analyzer_app.get(
    "/get_available_symbols",
    description="API to lookup a stock ticker by keywords",
    response_model=list[MetaDataSchema],
)
async def get_available_symbols():
    try:
        mongo_query_manager = QueryManager()
        result = await mongo_query_manager.get_available_symbols()

        return result
    except:
        raise HTTPException(status_code=404, detail="Something went wrong")


@data_analyzer_app.get(
    "/symbol_lookup/{keywords}",
    description="API to lookup a stock ticker by keywords",
    response_model=list[SymbolLookUpResponse],
    response_model_by_alias=False,
)
async def look_up_symbol(keywords: str):
    try:
        data_fetcher = ExternalDataFetcher()
        result = await data_fetcher.search_for_symbol(keywords=keywords)

        return result
    except:
        raise HTTPException(status_code=404, detail="Something went wrong")


def send_message_to_collector(message: str):
    message_queue = MessagingQueue()
    message_queue.send_message(message_body=message)
    # after it is sent just ping the collector service to receive the message.
    requests.get(f"{settings.collector_service_url}/load_symbol_data")


@data_analyzer_app.get(
    "/get_symbol_data/{symbol}",
    description="API to lookup a stock ticker data",
    response_model=EfficientDataResponse,
)
async def get_symbol_data_for_user(symbol: str):
    try:
        result = []
        data_formatter = Utils()
        mongo_query_manager = QueryManager()
        source = None

        # 1. check if data exist in mongo or not.
        data_missing = await mongo_query_manager.check_if_data_is_missing_or_stale(
            symbol=symbol
        )
        # 2. if data does not exist in mongo or is stale, send data to user from the externalapi directly (so user don't have to wait).
        if data_missing is True:
            # TODO: Add message to the queue to collect the date so its available in internal database next time user selects the same ticker.
            send_message_to_collector(message=symbol)

            # continue to send data from api in the meanwhile
            data_fetcher = ExternalDataFetcher()
            external_result = await data_fetcher.get_data_for_symbol(symbol=symbol)
            validated_external_data = ExternalResponseDataSchema(**external_result)
            result = data_formatter.standardize_external_data(validated_external_data)
            source = "external"

        else:
            result = await mongo_query_manager.get_symbol_data(symbol=symbol)
            source = "internal"

        result = data_formatter.return_efficient_response(result)
        result["source"] = source

        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Something went wrong")


# Prometheus Metrics
metrics_app = make_asgi_app()
data_analyzer_app.mount("/metrics", metrics_app)

# MODAL CLOUD DEPLOYMENT ATTRIBUTES: Basically we are attaching our app instance to modal serverless function. (No impact on local running)
app = modal.App("data_analyzer")

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
        "pydantic-settings",
        "pandas",
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
    return data_analyzer_app
