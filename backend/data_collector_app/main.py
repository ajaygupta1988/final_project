import sys, os
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import make_asgi_app
import modal

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
from components import QueryManager, ExternalDataFetcher
from schemas import ExternalResponseDataSchema


data_collector_app = FastAPI()

instrumentator = Instrumentator().instrument(data_collector_app)


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
    "/load_symbol_data/{symbol}",
    description="API endpoint to load stock ticker data in mongo database",
)
async def load_symbol_data(symbol: str):
    # TODO: ADD messaging queue consumer and get the symbol value from the queue. Its an overkill but for sake of learning
    try:
        mongo_query_manager = QueryManager()
        update_required = await mongo_query_manager.check_if_data_is_missing_or_stale(
            symbol=symbol
        )

        if update_required is True:
            data_fetcher = ExternalDataFetcher()
            vantage_api_response_data = await data_fetcher.get_data_for_symbol(
                symbol=symbol
            )
            result = await mongo_query_manager.add_data_from_api(
                data=ExternalResponseDataSchema(**vantage_api_response_data)
            )

        return {"detail": "Data succesfully loaded for data analyzer service."}
    except:
        raise HTTPException(status_code=404, detail="Something went wrong")


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
    return data_collector_app
