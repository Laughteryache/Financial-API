import time

from fastapi import FastAPI, Request
from fastapi_versioning import VersionedFastAPI

from src.deposits.router import router as deposits_router
from src.targets.router import router as target_router
from src.users.router import router as users_router
from src.logger import logger

# General module

app = FastAPI(title="FinAPI")


app.include_router(users_router)
app.include_router(deposits_router)
app.include_router(target_router)


# For logger
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request execution time", extra={
        'process_time': round(process_time, 4)
    })
    return response


# For API versioning
app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}'
)
