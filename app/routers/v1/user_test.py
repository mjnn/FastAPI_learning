from fastapi import APIRouter, Body
from typing import Annotated
from app.schemas.user_test import UserForCreate
from app.services.user_test import hash_password
from app.models.user_test import DbUserModel
from app.db.session import SessionDep

router = APIRouter(
    prefix="/user_test",
    tags=["user_test"]
)

@router.post("/create_user", response_model=DbUserModel)
def create_user_router(
        user: Annotated[
            UserForCreate,
            Body(
                examples=[
                    {
                        "username": "user",
                        "email": "user@example.com",
                        "password": "User123!"
                    }
                ],
            )],
        session: SessionDep):
    user = hash_password(user)
    db_user = DbUserModel(
        username=user.username,
        email=user.email,
        hashed_password=user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user