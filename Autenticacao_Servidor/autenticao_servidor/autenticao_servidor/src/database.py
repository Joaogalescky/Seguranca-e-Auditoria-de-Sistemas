from sqlalchemy import Session, create_engine

from .settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with AsyncSession(engine, expire_on_commit=False) as session:
        yield session