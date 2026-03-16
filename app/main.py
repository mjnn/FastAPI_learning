from fastapi import FastAPI,Request
from app.routers.v1 import get_post_test, user_test
from app.core.config import settings
from app.core.exception import request_validation_handler, sqlmodel_validation_handler,AlreadyExistException
from app.core.response import ResponseModel
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from sqlmodel import create_engine, SQLModel
from app.db.session import create_db_and_tables
from sqlalchemy.exc import (
    IntegrityError,  # 主键冲突、唯一约束冲突等
    SQLAlchemyError,  # SQLAlchemy 基础异常（兜底）
    NoResultFound,    # 查询无结果
    MultipleResultsFound  # 查询返回多条结果
)
# 实例化FastAPI
app = FastAPI()

# 注册请求参数的类型验证错误
app.exception_handler(RequestValidationError)(request_validation_handler)
app.exception_handler(AlreadyExistException)(request_validation_handler)
app.exception_handler(IntegrityError)(sqlmodel_validation_handler)

# 注册路由
app.include_router(
    get_post_test.router,
    prefix=settings.API_V1_STR
)


app.include_router(
    user_test.router,
    prefix=settings.API_V1_STR
)

# 启动时同时创建数据库和相关表模型
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get('/')
def root():
    return ResponseModel(data='Here is Root!')