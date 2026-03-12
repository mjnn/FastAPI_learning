from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends
from app.core.config import settings

connect_args = {"check_same_thread": settings.CHECK_SAME_THREAD}
engine = create_engine(
    settings.SQLITE_URL,
    connect_args=connect_args
)
print(settings.SQLITE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]