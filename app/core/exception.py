from typing import Generic, TypeVar, Optional, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from sqlalchemy.exc import IntegrityError


class AlreadyExistException(Exception):
    """
    用于任何修改数据时遇到的已存在数据情况抛出的异常
    """
    pass

class DbOperationError(Exception):
    """
    用于任何数据库操作错误
    """
    pass

async def db_error_handler(request: Request, exc: DbOperationError):
    """
    用于处理数据库报错
    """
    return JSONResponse(
        status_code=500,
        content={
            "message": '数据库操作失败',
            "errors": exc.__str__(),
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    处理通用HTTP异常
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

async def request_validation_handler(request: Request, exc: Exception) -> JSONResponse:
    """处理请求参数验证错误（HTTP 422）"""
    # 格式化验证错误信息
    if isinstance(exc, RequestValidationError):
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
    elif isinstance(exc, AlreadyExistException):
        return JSONResponse(
            status_code=422,
            content={
                "message": '数据更新失败',
                "errors": exc.__str__(),
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
