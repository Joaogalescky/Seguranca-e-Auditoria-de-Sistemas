from typing import Union

from fastapi import FastAPI

from src.routers import user
from src.schemas import Message

app = FastAPI()

app.include_router(user.router)

@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {"Hello": "World"}
