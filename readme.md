## Project Overview
This project aims to compare historical prices of different stocks over a long period, and visualize them on a basic time series chart spanning several years. The API endpoint retrieves stock data from MongoDB, preloaded by a collector service. If the data is not available in MongoDB, it queries the external Vantage API and immediately responds to the user (to avoid user wait time). After responding, it sends a message to the collector service to load the data into MongoDB for future requests. This ensures that data is loaded only once, even if multiple users request the same stock (e.g., TSLA) simultaneously.

## Features
- Retrieve and compare historical stock prices over larger timeframe (20 years).
- Visualize stock data on a time series chart.
- Efficient data loading from MongoDB and external API.
- Minimized user wait time by loading data asynchronously.
- Single data load per stock symbol to optimize performance.

## External Stock API:
For this application I am using Alpha Vantage (https://www.alphavantage.co) a free public api to get the historical stock prices of a particular stock by Ticker (Example:TSLA). Their documentation is pretty simple and have API key based access.

## Techstack
- Database: MongoDB is used as persistance dtabase. Its a no sql database so requires minimal deployment efforts and ideal for datascience project where data structure of external service is unknown and unpredictable.
- Frontend: React web app interacting with a backend service. This will be hosted on aws Amplify with full CI/CD using amplify.yml file (In Progress)
- Backend: There are two seprate serverless backend services that you can run in parallel. Written is python using FastApi framework and deployed on Modal Serverless platform with full CI/CD pipline managed through Github Actions. It similar to aws Lambda but will minimal deployment effort. https://modal.com
  - Collector Service: To collect data and save it to MongoDB upon request. It will check if data exist or is stale and then update it on demand. The update trigger will be managed by simple messaging queue. 
  - Analyzer Service: This is a Rest Api service connected to the web application and have Api's to display data on the front end web application.

## See pdf file in the repo for system architecture.

# Basic Setup

To run this project, follow these steps:

1. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv .venv
    ```

2. Activate the virtual environment:

    - On Linux/macOS:

        ```bash
        source venv/bin/activate
        ```

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Environment File [very important]: Please go to backend/config and rename .env_local to .env before going on the next steps.

    ```bash
    ./backend/config and rename .env_local to .env before going on the next steps.
    ```


## Setting up local database with docker

To run this project locally you will also need to setup a local mongodb server, follow these steps:

1. Run docker-compose in one of your terminal: You can also see and connect to the local database though MongoDB Compass application. Docker will also spin up an aws local stack 

    ```bash
    docker-compose up
    ```

2. create aws messaging queue in your local environment

`aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name  data-collector-queue`

it should return the following: If you key is different please update QUEUE_URL

`QueueUrl": "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/data-collector-queue`

## Run tests

1. Backend Tests:

    ```bash
    pytest
    ```

2. Frontend Tests:

    ```bash
    cd frontend && npm run test
    ```


## Run Backend Servers


### Run Data Collector Service: 

Primary purpose of this service is to collect data from an external server and save it to our mongodb database. This service will not be connected to the frontend.

`uvicorn backend.data_collector_app.main:data_collector_app --host=0.0.0.0 --port=${PORT:-5000}`

Once the server is running, you can access the app at http://localhost:5000 (by default). Use tools like cURL, Postman, or your browser to interact with the endpoints.

- **GET /**: Health check api
- **GET /docs**: To see the swagger UI documentation for the service.
- **GET /metrics**: To see the prometheus metrics.
- **Get /load_symbol_data/{symbol}**: This is an endpoint to initita data loading for a STOCK (Example: http://localhost:5000/load_symbol_data/TSLA ). Max 20 years of monthly data is loaded if available. The endpoint itself returns a simple success message. To confirm is data is loaded you need to start the Data Analyzer app (Next Section) and use http://localhost:5000/get_symbol_data/TSLA api to retrive data.

Deployed app url: https://ajaygupta1988--data-collector-fastapi-app.modal.run/

### Run Data Analyzer/Web Service: 

This is a Rest Api service connected to the web application and have api's to display data on the front end web application.

`uvicorn backend.data_analyzer_app.main:data_analyzer_app --host=0.0.0.0 --port=${PORT:-5001}`

Make sure the PORT is different from collector app.
   
Once the server is running, you can access the app at http://localhost:5001 (by default). Use tools like cURL, Postman, or your browser to interact with the endpoints.

- **GET /**: Health check api
- **GET /docs**: To see the swagger UI documentation for the service.
- **GET /metrics**: To see the prometheus metrics.
- **GET /symbol_lookup/{keyord}**: API to lookup a stock ticker by keywords.
- **GET /available_symbols**: API to see what stock symbols data is already in the database.
- **Get /get_symbol_data/{symbol}**: This API endpoint retrieves stock symbol data from MongoDB, preloaded by a collector service. If the data is not available in MongoDB, it queries the external Vantage API and responds immediately to the user (to avoid user wait time). After responding, it sends a message to the collector service to load the data into MongoDB for future requests. This ensures that data is loaded only once, even if multiple users request the same stock (e.g., TSLA) simultaneously.

Deployed app url: https://ajaygupta1988--data-analyzer-fastapi-app.modal.run/docs

## Run Frontend application

Run the following commands:


    ```bash
    cd frontend && npm run dev
    ```


Once the server is running, you can access the web app at http://localhost:3001 (by default). Use tools like cURL, Postman, or your browser to interact with the endpoints.

Deployed Frontend app url: https://main.d20tk70v3b77bl.amplifyapp.com/

## Project Folder Structure
### Backend
1. components: Contains reusable modules and utilities that are shared between the data_collector_app and data_analyzer_app.
2. config: Stores configuration settings and environment variables.
3. data_analyzer_app: Manages the analysis of collected stock data, including comparison and visualization.
4. data_collector_app: Handles data collection from external APIs and populates the MongoDB database.
5. schemas: Defines data schemas and validation rules used across the backend applications.
6. .github for CI/CD pipes yml files.

### Frontend
1. frontend: Contains a React application for the front-end interface, allowing users to interact with the API and visualize stock data.

### Other
1. mongodb_data: (Directory not fully visible but likely) Contains MongoDB data files or database-related configurations.
2. .github: GitHub-specific files for workflows and actions.
3. docker-compose.yml: Docker Compose file for setting up and running local MongoDB.
4. prometheus.yml: Configuration file for Prometheus, likely used for monitoring and metrics.

## CI/CD
All apps are deployed on their respective cloud service using CI/CD pipeline.
 - Backend deployments are handled using github actions. .github folder has all the files.
 - Frontend is deployed on AWS amplify which connects to github repo directly. Look form amplify yml file in frontend directory.


 ## Metrics with Promethues
 I have also implemented basic level of metrics with prometheus. Grafana will do in future.


 ## Messaging Queue 
 Also want to reiterate that messaging queue is implemented using AWS SQS service. You can test it by loading a ticker from a search bar when the data is loaded first time it will tell you the source. 

 check and uncheck the same ticker again you will see that data is now coming from mongo db. This happened because when you initally added a stock the date was fetched from the api but the analyzer also added the message to the queue to tell collecter to get the data for the user next time.