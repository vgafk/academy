import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from api import routers
from settings import settings

from sql import init_models

app = FastAPI(title='vgafkAPI',
              version='0.1 Alpha',
              description='vgafkAPI - API Волгоградской академии физической культуры')

[app.include_router(router, prefix='/api') for router in routers]


# @app.router.get('/', include_in_schema=False)
# def index() -> RedirectResponse:
#     return RedirectResponse('/docs')


if __name__ == '__main__':
    if settings.NEED_NEW_BASE:
        asyncio.run(init_models())
    uvicorn.run('main:app', reload=True, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
