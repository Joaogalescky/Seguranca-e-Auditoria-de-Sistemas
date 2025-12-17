from http import HTTPStatus

from fastapi import FastAPI, Request

from .mtls_middleware import MTLSMiddleware
from .routers import auth, user
from .schemas import Message

app = FastAPI()

app.add_middleware(MTLSMiddleware)

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello World"}

@app.get("/cert-info")
def get_cert_info(request: Request):
    return {
        'client_cn': getattr(request.state, 'client_cn', 'not-available'),
        'mtls_validated': getattr(request.state, 'mtls_validated', False),
        'has_cert': hasattr(request.state, 'client_cert'),
    }