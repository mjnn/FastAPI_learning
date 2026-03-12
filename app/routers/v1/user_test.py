from fastapi import APIRouter, Body, HTTPException
from typing import Annotated
from app.schemas.user_test import UserForCreate
from app.services.user_test import hash_password
from app.models.user_test import DbUserTable
from app.db.session import SessionDep
from app.core.response import BaseResponseModel, success_response, error_response
from sqlmodel import select

router = APIRouter(
    prefix="/user_test",
    tags=["user_test"]
)

@router.post("/create_user", response_model=BaseResponseModel)
def create_user(
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
    db_user = DbUserTable(
        username=user.username,
        email=user.email,
        hashed_password=user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return success_response(f'用户{db_user.username}创建完成！')

@router.get("/read_user", response_model=BaseResponseModel)
def read_user(username: str, session: SessionDep):
    statement = select(DbUserTable).where(DbUserTable.username == username)
    user = session.exec(statement).first()  # first() 取第一条，无结果返回 None
    if not user:
        return error_response(http_code=404, errors=f'用户{username}不存在！')
    return success_response(f'用户{user.username}数据如下：{user.model_dump()}')