import asyncio

from fastapi import FastAPI

from strawberry.fastapi import GraphQLRouter
from strawberry.federation import Schema
from strawberry.schema.config import StrawberryConfig

from api.queryes import Query
from api.types import User, Student
from db import init_models

app = FastAPI()

schema = Schema(query=Query, types=[User, Student], enable_federation_2=True,
                config=StrawberryConfig(auto_camel_case=False))


graphql_router = GraphQLRouter(schema)
app.include_router(graphql_router, prefix="/graphql")

if __name__ == '__main__':
    asyncio.run(init_models())
