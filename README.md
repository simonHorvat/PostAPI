# PostAPI

PostAPI is a web service built with FastAPI that allows users to perform CRUD (Create, Read, Update, and Delete) operations on blog posts. The service utilizes SQLAlchemy as an ORM tool to enable interaction with a SQLite database. At the start of the application, the database is initialized with toy data (`@app.on_event("startup")` event in run.py).

## Running the API with Docker

To run the API using Docker, follow these steps:

1. Install Docker on your machine if it is not already installed.
2. Clone this repository to your local machine.
3. Navigate to the root directory of the project in your terminal or command prompt.
4. Build the Docker image by running the following command: ```docker build -t post-api .```
5. Run the Docker container by running the following command: ```docker run -p 8000:8000 post-api```
6. The API should now be running on http://localhost:8000/. Swagger documentation is available on http://localhost:8000/docs.

## Running without Docker
To run the API without using Docker, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the root directory of the project in your terminal or command prompt.
3. Install the required dependencies by running the following command: ```pip install -r requirements.txt```
4. Start the API by running the following command: ```python run.py```
The API should now be running on http://localhost:8000/. Swagger documentation is available on http://localhost:8000/docs.

## Project Structure

The project has the following structure:
```
PostAPI
│   config.ini
│   Dockerfile
│   requirements.txt
│   run.py
│
├───app
│   │   main.py
│   │   utils.py
│   │   __init__.py
│   │
│   └───routes
│           posts.py
│
├───database
│       database.py
│       load_data.py
│       models.py
│       __init__.py
│
└───schemas
        info_message_schema.py
        post_schema.py
```

Files description:

- `config.ini`: This file contains configuration parameters for the API, such as the database connection string.
- `Dockerfile`: This file contains instructions for building a Docker image of the API.
- `requirements.txt`: This file contains the Python dependencies required to run the API.
- `run.py`: This file is the entry point for the API, and is used to start the FastAPI application.
- `app/main.py`: This file contains the FastAPI application, and is where the API routes are defined.
- `app/utils.py`: This file contains utility functions used by the API.
- `app/routes/posts.py`: This file contains the API routes for interacting with blog posts.
- `database/database.py`: This file contains the SQLAlchemy database connection and session objects.
- `database/load_data.py`: This file contains functions for loading data into the database.
- `database/models.py`: This file contains the SQLAlchemy models for the database tables.
- `schemas/info_message_schema.py`: This file contains the Pydantic schema for returning informational messages.
- `schemas/post_schema.py`: This file contains the Pydantic schema for blog posts.
