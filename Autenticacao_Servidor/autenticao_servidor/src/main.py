from http import HTTPStatus

from fastapi import FastAPI

from src.routers import auth, user
from src.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"Hello": "World"}
