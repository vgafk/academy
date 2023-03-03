import uvicorn


if __name__ == '__main__':
    uvicorn.run('server:app', reload=True, host=settings.SERVER_HOST, port=settings.SERVER_PORT)