from typing import Generic, TypeVar, Optional, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from sqlalchemy.exc import IntegrityError

# 泛型类型定义
T = TypeVar("T")


class ResponseModel(GenericModel, Generic[T]):
    """基础响应模型（无code字段，code作为HTTP状态码）"""
    message: str = Field('success', description="返回消息")
    data: Optional[T] = Field(None, description="返回数据")


# -------------------------- 异常处理器改造 --------------------------

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    处理通用HTTP异常
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

async def request_validation_handler(request: Request, exc: RequestValidationError):
    """处理请求参数验证错误（HTTP 422）"""
    # 格式化验证错误信息
    custom_errors = []
    for error in exc.errors():
        custom_errors.append({
            "field": ".".join(error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    # 返回422 HTTP状态码 + 自定义错误格式
    return JSONResponse(
        status_code=422,
        content={
            "message" : '参数验证失败',
            "errors" : custom_errors,
        }
    )

async def sqlmodel_validation_handler(request: Request, exc: IntegrityError):
    """处理数据库约束错误（HTTP 400）"""
    # 解析异常信息
    if "UNIQUE constraint failed" in str(exc):
        if "dbusertable.username" in str(exc):
            message = "用户名已存在"
        elif "dbusertable.email" in str(exc):
            message = "邮箱已被注册"
        else:
            message = "数据重复，无法创建/更新"
    else:
        message = "数据库约束错误，请检查输入数据"

    return JSONResponse(
        status_code=400,
        content={
            "message" : message,
            "errors" : str(exc.orig),
        }
    )
