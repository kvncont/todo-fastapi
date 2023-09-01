"""Main"""

import os
from contextlib import asynccontextmanager

from azure.cosmos.aio import CosmosClient
from fastapi import FastAPI

from app.routers import todos

DATABASE_NAME = os.environ["DATABASE_NAME"]
CONTAINER_NAME = os.environ["CONTAINER_NAME"]
URI = os.environ["COSMOSDB_ENDPOINT"]
KEY = os.environ["COSMOSDB_KEY"]


@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Context manager to handle application lifespan events.
    """

    application.state.cosmos_client = CosmosClient(URI, credential=KEY)
    application.state.database = (
        await application.state.cosmos_client.create_database_if_not_exists(
            DATABASE_NAME
        )
    )
    application.state.container = (
        await application.state.database.create_container_if_not_exists(
            CONTAINER_NAME, "/id"
        )
    )

    yield

    application.state.cosmos_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router=todos.router, prefix="/todos", tags=["ToDo"])
