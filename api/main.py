from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.db import connection as db
from src.api import incoming


@asynccontextmanager
async def lifespan(_):
    await db.setup("sqlite+aiosqlite:///:memory:")
    yield
    await db.teardown()

app = FastAPI(lifespan=lifespan)
app.include_router(incoming.router, prefix='/api/v1/incoming')

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
