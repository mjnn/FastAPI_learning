from typing import Optional, Annotated
from pydantic import BaseModel
from app.schemas.user_test import UserForCreate
from fastapi import Body, HTTPException
from app.services.user_test import hash_password
from app.db.session import SessionDep
from app.models.user_test import DbUserTable
from app.schemas.user_test import UserForCreate
from app.schemas.user_test import db_user_query
from sqlmodel import select

def db_create_user(
        user: UserForCreate,
        session: SessionDep
)-> DbUserTable:
    """

    :param user: 用户模型
    :param session: 数据库操作会话
    :return: 操作完成的用户数据库模型
    """
    user = hash_password(user)
    db_user = DbUserTable(
        username=user.username,
        email=user.email,
        hashed_password=user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def db_read_user(
        query_dict: db_user_query,
        session: SessionDep
) -> DbUserTable | None:
    """
    根据指定字段和值查询用户信息

    :param query_dict: 用来查询的键值对（包含query_field和query_value属性），如：query_field='username', query_value='user'
    :param session: 数据库操作会话
    :return: 查询到的用户对象，无结果返回 None
    """
    # 获取表的所有字段名
    all_field_names = [column.name for column in DbUserTable.__table__.columns]
    query_field = query_dict.query_field
    query_value = query_dict.query_value

    # 1. 校验查询字段是否存在
    if query_field not in all_field_names:
        raise ValueError(f"查询字段 '{query_field}' 不存在于 DbUserTable 中，有效字段：{all_field_names}")

    # 2. 动态获取表的字段
    table_field = getattr(DbUserTable, query_field)

    # 3. 执行查询
    statement = select(DbUserTable).where(table_field == query_value)
    user = session.exec(statement).first()  # first() 取第一条，无结果返回 None

    return user


def db_update_user(
        user: DbUserTable,
        session: SessionDep
)-> DbUserTable:
    query_dict = {
        'query_field': 'username',
        'query_value': user.username,
    }
    db_user = db_read_user(query_dict, session)
    if not db_user:
        return None