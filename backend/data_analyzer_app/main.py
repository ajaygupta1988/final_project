import sys, os
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import make_asgi_app
import modal

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from components import ExternalDataFetcher, QueryManager, Utils
from schemas import (
    SymbolLookUpResponse,
    ExternalResponseDataSchema,
    EfficientDataResponse,
)


data_analyzer_app = FastAPI()

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
    "/symbol_lookup/{keywords}",
    description="API to lookup a stock ticker by keywords",
    response_model=list[SymbolLookUpResponse],
)
async def look_up_symbol(keywords: str):
    try:
        data_fetcher = ExternalDataFetcher()
        result = await data_fetcher.search_for_symbol(keywords=keywords)

        return result
    except:
        raise HTTPException(status_code=404, detail="Something went wrong")


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
            data_fetcher = ExternalDataFetcher()
            external_result = await data_fetcher.get_data_for_symbol(symbol=symbol)
            validated_external_data = ExternalResponseDataSchema(**external_result)
            result = data_formatter.standardize_external_data(validated_external_data)
            source = "external"

            # TODO: Add message to the queue to collect the date so its available in internal database next time user selects the same ticker.
        else:
            result = await mongo_query_manager.get_symbol_data(symbol=symbol)
            source = "internal"

        result = data_formatter.return_efficient_response(result)
        result["source"] = source

        return result
    except:
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
    ]
)


# attaching app to serverless function
@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("mongodb-secret"),
        modal.Secret.from_name("vantage_api_key"),
    ],
)
@modal.asgi_app()
def fastapi_app():
    return data_analyzer_app