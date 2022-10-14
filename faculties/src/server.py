import asyncio

from fastapi import FastAPI

from strawberry.fastapi import GraphQLRouter
from strawberry.federation import Schema

from api.queryes import Query
from api.types import Group, Student
from db import init_models

app = FastAPI()

schema = Schema(query=Query, types=[Group, Student], enable_federation_2=True)


graphql_router = GraphQLRouter(schema)
app.include_router(graphql_router, prefix="/graphql")

if __name__ == '__main__':
    asyncio.run(init_models())
