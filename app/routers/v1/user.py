from fastapi import APIRouter, Body, HTTPException, status
from typing import Annotated
from app.schemas.user_test import UserForCreate, db_user_query, UserForUpdate
from app.db.session import SessionDep
from app.db.crud import db_create_user, db_read_user, db_update_user, db_delete_user
from app.core.response import ResponseModel

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post(
    "/create_user",
    response_model = ResponseModel,
    status_code = status.HTTP_200_OK ,
)
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
    """
    创建用户/注册用户接口
    """
    db_user = db_create_user(user,session)
    return ResponseModel(data=f'用户{db_user.username}创建完成！')

@router.post("/query_user", response_model=ResponseModel,status_code = status.HTTP_200_OK)
def query_user(
        query_dict: Annotated[
            db_user_query,
            Body(
                openapi_examples = {
                    '使用username查询':{
                        'value':{
                            'query_field': 'username',
                            'query_value': 'user',
                        }
                    },
                    '使用邮箱查询':{
                        'value': {
                            'query_field': 'email',
                            'query_value': 'user@example.com',
                        }
                    },
                    '使用userid查询':{
                        'value':{
                            'query_field': 'userid',
                            'query_value': 1,
                        }
                    }
                }
            )
        ] ,
        session : SessionDep
):
    """
    根据指定字段和值查询用户信息
    """
    user = db_read_user(query_dict, session)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "message": '请求失败！',
                "errors" : f'用户{query_dict.query_field}不存在！'
            }
        )
    user.updated_at = user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    user.created_at = user.created_at.strftime('%Y-%m-%d %H:%M:%S')
    return ResponseModel(data=user)


@router.put("/update_user", response_model=ResponseModel,status_code = status.HTTP_200_OK)
def update_user(userid: int,user_new : UserForUpdate, session: SessionDep):
    db_user = db_update_user(userid, user_new, session)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail={
                "message": '请求失败！',
                "errors": f'userid为{userid}的用户不存在！'
            }
        )

    return ResponseModel(data=db_user)

@router.delete("/delete_user", response_model=ResponseModel,status_code = status.HTTP_200_OK)
def delete_user(userid: int, session: SessionDep):
    db_user = db_delete_user(userid, session)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail={
                "message": '请求失败！',
                "errors": f'userid为{userid}的用户不存在！'
            }
        )

    return ResponseModel(data=db_user)