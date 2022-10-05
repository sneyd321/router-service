import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from models.query import Query
from models.mutation import Mutation
import uvicorn
import asyncio
import requests
from typing import AsyncGenerator, Optional, List
from models.graphql_types import House
from strawberry.types import Info
from fastapi.middleware.cors import CORSMiddleware


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_credentials=True,
 allow_origins=["*"], allow_headers=["*"], allow_methods=["*"]
)
app.include_router(graphql_app, prefix="/graphql")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)