from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import Token
from src.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])
Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session,
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}