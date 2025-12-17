from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_session
from ..models import User
from ..schemas import Token
from ..security import create_access_token, get_current_user, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2Form, session: Session,
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    access_token = create_access_token(data={'sub': user.email})
    refresh_token = create_refresh_token(data={'sub': user.email})
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }

@router.post('/refresh_token', response_model=Token)
def refresh_access_token(refresh_token: str):
    try:
        payload = decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
        email = payload.get('sub')
    except:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    
    new_access_token = create_access_token(data={'sub': email})
    new_refresh_token = create_refresh_token(data={'sub': email})
    
    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token,
        'token_type': 'bearer'
    }