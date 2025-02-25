from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from app.settings import Settings
from app.utils import make_amqp_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_amqp_consumer()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/health')
async def health_app():
    return {'health': 'ok'}


if __name__ == '__main__':
    uvicorn.run('app.main:app', host='0.0.0.0', port=8002,
                reload=True, env_file='.env')
