import uvicorn

if __name__ == "__main__":
    uvicorn.run("applications.data_collector.main:data_collector_app", host="127.0.0.1", port=8001, reload=True)