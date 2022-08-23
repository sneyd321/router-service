import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from query import Query
from mutation import Mutation
from resolver import zk
import uvicorn

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.on_event("startup")
async def startup_event():
    zk.initialize()
    zk.create_node()

@app.get("/")
def get_children():
    return zk.get_children()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)